# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp import models, fields, api, exceptions
from email.utils import formataddr
from cmislib.model import CmisClient, Repository
from cmislib.exceptions import CmisException
import tempfile
import base64
import types
import os
import zipfile
import shutil
import sys

class sale_devis(models.Model):
    _name = "sale.devis"
    _inherit = "sale.devis"
    _description = "Sales Devis"



######## ajouter
    @api.multi
    def _get_id_devis(self, context=None):
	print "context get id devis .........................",context
        return context.get('reference', False)


    @api.multi
    def _rapport_content_jasper(self):
	print "...........rapport_content_jasper.............",self
        obj_courant = self.env['sale.devis'].search([('reference', '=', self._get_id_devis(self.env.context))])
	
        data = {}
        data['records'] = self
	data['model']='sale.devis'
	print "........data",data,'........obj_courant.id',self.id
        sys.path.append(os.path.abspath("openerp/jasper_reports"))
        from jasper_report import * 
        r1 = report_jasper('report.Devis', 'sale.devis')
	print ".......r1",r1
        result = r1.create(self._cr, self.env.uid, self.id, data, self.env.context)
        rapport_binary = base64.encodestring(result[0])      
        return rapport_binary


    @api.multi
    def open_report_wizard(self, context):
	print "context .......",context
	partner_id = context.get('partner_id')
	uid = context.get('uid')
	email =self.env['res.partner'].browse(partner_id).email
	email_uid =self.env['res.partner'].browse(uid).email
	print "email ....",email_uid

	configs = self.env['office.alfresco.configuration'].search([('is_default', '=', 'True')])[0]
        url = configs.url
        port = configs.port
        user = configs.user
        mp = configs.mp

        try:
            client = CmisClient('http://' + url + ':' +
                                repr(port) + '/alfresco/service/cmis', user, mp)
            repo = client.defaultRepository
        except:
            print 'failed to connect to Alfresco'
            quit()

	objet = 'Devis '+ self.reference
	print "objet .......",objet
        self.env.cr.execute("DELETE FROM mail_wiz") 
        self.env.cr.execute("INSERT INTO mail_wiz(id, objet, email, email_from) VALUES(%s,%s,%s,%s)",('1',objet,email,email_uid))

#  *** debut recuperation du rapport ---------------------------------------------------------------
        document_wiz_rapport = self.env['document_wiz'].create({'data': self._rapport_content_jasper(),'nom_fichier':'Devis ' + self.reference+ '.pdf'})

	ir_attachement_rapport = self.env['ir.attachment'].create({'datas': self._rapport_content_jasper(),'datas_fname':'devis ' + self.reference  + '.pdf','name':'Devis ' + self.reference + '.pdf', 'res_model':self._name})

        self.env.cr.execute("INSERT INTO document_wiz_mail_wiz_rel VALUES('1','" + repr(document_wiz_rapport[0].id) + "')")
#  &&&& Fin recuperation du rapport -----------------------------------------------------------------


#  *** debut recuperation des documents -------------------------------------------------------------
        obj_courant = self.env['sale.devis'].search([('reference', '=', self._get_id_devis(self.env.context))])
	print "reference obj courant=====",obj_courant.reference,'.....',self.reference,'self...',self.id
	products_list = self.devis_lines
	print "produits===", products_list
	for product in products_list:
		product_obj = product.product_id
		print "product id===", product_obj
		print "id===", product_obj.id
        	documents_product = self.env['office.document.alfresco.produit'].search([('produit_id', '=', product_obj.product_tmpl_id.id)])
		print "document id ======", documents_product
		for document in documents_product:
		    doc = repo.getObject(document.node)
		    result = doc.getContentStream()
		    fobj = tempfile.NamedTemporaryFile(delete=False)
		    fname = fobj.name
		    fobj.write(result.read())
		    fobj.close()

		    file_base64 = ''
		    with open(fname, "rb") as file:
		        file_base64 = base64.encodestring(file.read())
		        document_wiz_piece_jointe = self.env['document_wiz'].create({'data':file_base64,'nom_fichier':document.nom_fichier})
		        self.env.cr.execute("INSERT INTO document_wiz_mail_wiz_rel VALUES('1','" + repr(document_wiz_piece_jointe[0].id) + "')")
			ir_attachement_rapport = self.env['ir.attachment'].create({'datas': file_base64,'datas_fname':document.nom_fichier,'name':document.nom_fichier, 'res_model':self._name})
#  &&&& Fin recuperation des documents -----------------------------------------------------------------
     
	
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail_wiz',
            'res_id':  int(1),            
            'view_id ref= report_wizard_form_view1': True,
            'type': 'ir.actions.act_window',
            'target': 'new',

        }


class document_wiz(models.TransientModel):
    _name = 'document_wiz'
    data = fields.Binary()
    nom_fichier = fields.Char(string="Nom du fichier")





class mail_wiz(models.TransientModel):
    _name = 'mail_wiz'

    email = fields.Char(string="À (Fournisseur)", required=True)
    email_from = fields.Char('De')
    objet = fields.Char(string = "Sujet", required=True)
    corps = fields.Text()

    state = fields.Selection([
            ('outgoing', 'Brouillon'),
            ('sent', 'Envoyé'),
            ('cancel', 'Annulé'),
        ], 'Status', default='outgoing')

    #  @api.multi
    #  def _rapport_et_pieces_jointes(self):
    #  return
    document_ids = fields.Many2many('document_wiz',string="Pièces Jointes")


    def send_mail(self, cr, uid, ids, context=None):
	print ".....................send mail"
        all_mail_wiz =  self.pool.get('mail_wiz').search(cr, uid, [('id',"=", 1)] ,context=context)

        mail_values = self.get_mail_values(cr, uid, context=context)
                # for res_id, mail_values in all_mail_values.iteritems():
                #     if wizard.composition_mode == 'mass_mail':
        email_id = self.pool['mail.mail'].create(cr, uid, mail_values, context=context)

        # self.pool['mail.mail'].write(cr, uid, email_id, 'attachment_id': [(6, 0, self._get_selection(cr, uid, context=context))]}, context=context)
        self.pool['mail.mail'].send(cr, uid,email_id,context=context)

        delete_attachement = cr.execute("DELETE FROM ir_attachment WHERE res_model='sale.devis'") 
	print '.........ids',ids
	tt = self.pool.get('sale.devis').write(cr,uid,ids, {'state': 'sent'},context)
	print "............................send",tt

        return {'type': 'ir.actions.act_window_close'}


    def get_mail_values(self, cr, uid, context=None):
        all_mail_wiz =  self.pool.get('mail_wiz').search(cr, uid, [('id',"=", 1)] ,context=context)

        attachment_id=self.pool.get('ir.attachment').search(cr, uid, [('res_model',"=", 'sale.devis')] ,context=context)
	print "attachment_id......",attachment_id
        mesaage = self.pool.get('mail_wiz').browse(cr, uid, all_mail_wiz, context=context)[0].corps
        email_vals = {}
        mail_values = {
           'subject':self.pool.get('mail_wiz').browse(cr, uid, all_mail_wiz, context=context)[0].objet,
           'email_to': self.pool.get('mail_wiz').browse(cr, uid, all_mail_wiz, context=context)[0].email,
           'email_from': 'contact@eps-tunisie.com',
           'body_html':mesaage.encode('utf-8'),
           'attachment_ids':[(6, 0, attachment_id)],

            }
	print "mail_values........",mail_values
            # mass mailing: rendering override wizard static values
        return mail_values








