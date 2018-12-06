# -*- coding: utf-8 -*-

from openerp import models, fields, api
import tempfile
import base64

class Document_produit(models.Model):
	_name = 'office.document.alfresco.produit'

	node = fields.Char(required=True)
	nom_fichier = fields.Char(string="Nom de fichier", required=True)
	description = fields.Text(string="Description")
	product_default_code = fields.Char(related='produit_id.default_code', store=True,string="Référence interne du produit",readonly=True)
	produit_id = fields.Many2one('product.template',ondelete='cascade', string="Designation du produit", readonly=True)


	@api.multi
	def unlink(self):
		repo = self.env['office.alfresco.configuration'].connection_alfresco()
		try:
			doc = repo.getObject(self.node)
			doc.delete()
		except:
			pass
		finally:
			models.Model.unlink(self)

	@api.multi
	def download_document(self):
		repo = self.env['office.alfresco.configuration'].connection_alfresco()

		doc = repo.getObject(self.node)
		doc_content = doc.getContentStream()

		file_obj = tempfile.NamedTemporaryFile(delete=False)
		file_name = file_obj.name
		file_obj.write(doc_content.read())
		file_obj.close()

		file_base64 = ''
		with open(file_name, "rb") as file:
			file_base64 = base64.encodestring(file.read())

		download_wizard_record = self.env['office.download.wizard'].create({'download_link' :file_base64 ,'nom_fichier':self.nom_fichier})

		return {
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'office.download.wizard',
			'res_id': int(download_wizard_record),
			'type': 'ir.actions.act_window',
			'target': 'new',
		}


class product(models.Model):
	_name='product.template'
	_inherit = 'product.template'

	document_ids = fields.One2many('office.document.alfresco.produit', 'produit_id', string='Documents')

	# salwa ksila update 24/03/2017
	@api.multi
	def ajout(self):
		return {
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'office.document.alfresco.product.wizard',
			'view_id ref="wizard_form_view1"': True,
			'type': 'ir.actions.act_window',
			'target': 'new',
		}