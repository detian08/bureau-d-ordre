# -*- coding: utf-8 -*-

from datetime import date, datetime
from dateutil import relativedelta
from openerp import tools, api
from openerp.osv import fields, osv
from openerp.exceptions import Warning
from openerp.exceptions import except_orm
from pyjarowinkler import distance

class res_partner_request(osv.osv):
	_name="res.partner.request"

	@api.model
	def _lang_get(self):
		languages = self.env['res.lang'].search([])
		return [(language.code, language.name) for language in languages]

	def __get_membership_state(self, *args, **kwargs):
		return self._membership_state(*args, **kwargs)

	_columns = {
		'operator_id':fields.many2one('res.partner'),
		'distance_ids': fields.one2many('res.partner.distance', 'partner_request_id', 'Distances'),
		'codif_infocham':fields.integer('Code infocham'),
        'parent_id': fields.many2one('res.partner', 'Société', select=True),
        'name': fields.char("Nom", required=True, select=True),
        'function': fields.char("Poste occupé", select=True),
        'category_id': fields.many2many('res.partner.category', id1='partner_id', id2='category_id', string="Secteurs d'activité",select=True),
        'street': fields.char('Rue', select=True),
		'note': fields.text(),
        'street2': fields.char('Street2'),
        'zip': fields.char('Code postale', size=24, change_default=True),
        'city': fields.char('Ville'),
        #'state_id': fields.many2one("res.country.state", 'State', ondelete='restrict'),
        'email': fields.char('Courriel'),
        'phone': fields.char('Tél.'),
        'fax': fields.char('Fax'),
        'mobile': fields.char('Tél. portable'),
		'matricule_fiscale' : fields.char("Numéros fiscal"),
		'code_tva' : fields.char("Registre de commerce"),
		'is_company': fields.boolean(help="Check if the contact is a company, otherwise it is a person"),
        'comment': fields.text('Notes'),
        'active': fields.boolean('Active'),
        'customer': fields.boolean('Customer', help="Check this box if this contact is a customer."),
        'supplier': fields.boolean('Supplier', help="Check this box if this contact is a supplier. If it's not checked, purchase people will not see it when encoding a purchase order."),
        'ref': fields.char('Contact Reference', select=1),
        'lang': fields.selection(_lang_get, 'Language',
            help="If the selected language is loaded in the system, all documents related to this contact will be printed in this language. If not, it will be English."),
        'date': fields.date('Date', select=1),
        'user_id': fields.many2one('res.users', 'Salesperson', help='The internal user that is in charge of communicating with this contact if any.'),
        'company_id': fields.many2one('res.company', 'Société', select=1),
        'state': fields.selection(
	[
            ('draft', 'Brouillon'),
            ('to_validate', 'En attente de validation'),
	    ('validate', 'Validée'),
	    ('reject', 'Refusée'),
        ], 'Status',help="Gives the status of the product.",select=True),
        'website': fields.char('Site Web', help="Website of Partner or Company"),
        'user_ids': fields.one2many('res.users', 'partner_id', 'Users'),
        'title': fields.many2one('res.partner.title', 'Civilité'),
        'country_id': fields.many2one('res.country', 'Pays', ondelete='restrict'),
		'use_parent_address': fields.boolean(u"Utiliser l'adresse de la société",help="Select this if you want to set company's address information  for this contact"),

    }
	_defaults = {
        'state': 'draft',
		'active':True,

    }
	@api.multi
	def onchange_type(self, is_company):
		value = {'title': False}
		if is_company:
			value['use_parent_address'] = False
			domain = {'title': [('domain', '=', 'partner')]}
		else:
			domain = {'title': [('domain', '=', 'contact')]}
		return {'value': value, 'domain': domain}

	#onchange contact/operateur
	def	partner_change(self, cr, uid, ids, operator_id, context=None):
		list_categ = []



		if operator_id :
			company_id = self.pool.get('res.partner').browse(cr,uid,operator_id,context=context).is_company

			if company_id == True:
				cr.execute("SELECT category_id FROM res_partner_res_partner_category_rel WHERE partner_id =%s",(operator_id,))
				lines = cr.dictfetchall()
				for line in lines :
					category_id= line['category_id']

					list_categ.append(category_id)

				return {'value': {
						'name': self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).name,
						'category_id':list_categ,
						'function': self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).function,
						'parent_id': self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).parent_id,
						'country_id':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).country_id.id,
						'street':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).street,
						'mobile':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).mobile,
						'website':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).website,
						'city':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).city,
						'zip':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).zip,
						'fax':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).fax,
						'email':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).email,
						'phone':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).phone,
						#'title':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).title,
						'is_company':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).is_company,
						'matricule_fiscale':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).vat,
						'code_tva':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).registre
					}}
			else:
				return {'value': {
						'name': self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).name,
						#'category_id':list_categ,
						'function': self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).function,
						'parent_id': self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).parent_id,
						'country_id':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).country_id.id,
						'street':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).street,
						'mobile':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).mobile,
						'website':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).website,
						'city':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).city,
						'zip':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).zip,
						'fax':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).fax,
						'email':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).email,
						'phone':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).phone,
						#'title':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).title,
						'is_company':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).is_company,
						'matricule_fiscale':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).vat,
						'code_tva':self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).registre,
						'use_parent_address' : self.pool.get('res.partner').browse(cr, uid, operator_id, context=context).use_parent_address,
					}}
		   
	#------------ Workflow opérateur économique --------------



	def draft_to_validate(self, cr, uid, ids, context=None):
		user_partner=self.pool.get('res.users').browse(cr, uid, uid, context=context).partner_id.id
		if uid == 1 :
			raise osv.except_osv(('Administrator!'),('Vous pouvez créer les opérateurs et ses contacts depuis le menu CRM/Opérateurs économiques.'))
		else :
			#notif Responsable
			op_id=self.browse(cr, uid, ids, context=context).id
			vals = {
				# 'subject':'Demande de validation',
				'record_name': "Validation d'une demande d'ajout d'un opérateur économique",
				'body':"<html> Merci de valider la demande d'ajout d'un opérateur économique </html>",
				'res_id':op_id,
				'reply_to':user_partner,
				'author_id':user_partner,
				'model':'res.partner.request',
				'type':'notification',
				'email_from':user_partner,
				'starred':True,
			}


			#get the parent id of the chef
			#user_id=self.pool.get('resource.resource').search(cr, uid,[('user_id','=',uid)], context=context)
			#section_id = self.pool.get('crm.case.section').search(cr, uid, [('member_ids','=',uid)],context=context)
			#print 'section_id .......',section_id
			#employee_id=self.pool.get('hr.employee').browse(cr, uid, uid, context=context).parent_id.id
			#name=self.pool.get('hr.employee').browse(cr, uid, employee_id, context=context).name_related
			#partner_id=self.pool.get('res.partner').search(cr, uid,[('name','=',name)], context=context)
			#print 'partner_id.....',partner_id
			mail_notif_vals = {
				'partner_id':3,
				'message_id':self.pool.get('mail.message').create(cr, uid, vals, context=context),
				'is_read':False,
				'starred':True,
			}

			self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)



		return self.write(cr, uid, ids, {'state': 'to_validate'})



	#update by Marwa BM 13-09-2017 validate the request and create it in res.partner
	def to_validate(self, cr, uid, ids, context=None):   

		#notif qui crée l'opérateur
		op_id=self.browse(cr, uid, ids, context=context).id
		#du res partner 
		create_id=self.browse(cr, uid, op_id, context=context).create_uid.id

		vals = {
			'record_name': "Validation d'une demande d'ajout d'un opérateur économique",
			'body':"<html> L'opérateur économique a été validé </html>",
			'res_id':op_id,
			'reply_to':uid,
			'author_id':uid,
			'model':'res.partner.request',
			'type':'email',
			'email_from':uid,
			'starred':False,
		}


		mail_notif_vals = {
			'partner_id':self.pool.get('res.users').browse(cr, uid, create_id, context=context).partner_id.id,
			'message_id':self.pool.get('mail.message').create(cr, uid, vals, context=context) ,
			'is_read':False,
			'starred':False,

		}

		company_id = self.browse(cr,uid,op_id,context=context).is_company
		if company_id == True:
			val = {
				'name':self.browse(cr,uid,op_id,context=context).name,
				'is_company':self.browse(cr,uid,op_id,context=context).is_company,
				#'category_id':list_category_id,
				'function':self.browse(cr,uid,op_id,context=context).function,
				'email':self.browse(cr,uid,op_id,context=context).email,
				'country_id':self.browse(cr,uid,op_id,context=context).country_id.id,
				'mobile':self.browse(cr,uid,op_id,context=context).mobile,
				'fax':self.browse(cr,uid,op_id,context=context).fax,
				'street':self.browse(cr,uid,op_id,context=context).street,
				'website':self.browse(cr,uid,op_id,context=context).website,
				'code_tva':self.browse(cr,uid,op_id,context=context).code_tva,
				'parent_id':self.browse(cr,uid,op_id,context=context).parent_id.id,
				'phone':self.browse(cr,uid,op_id,context=context).phone,
				'city':self.browse(cr,uid,op_id,context=context).city,
				'street2':self.browse(cr,uid,op_id,context=context).street2,
				'title':self.browse(cr,uid,op_id,context=context).title.id,
				'vat' : self.browse(cr,uid,op_id,context=context).matricule_fiscale,
				'registre': self.browse(cr,uid,op_id,context=context).code_tva,
			}

		else:
			val = {
				'name':self.browse(cr,uid,op_id,context=context).name,
				'is_company':self.browse(cr,uid,op_id,context=context).is_company,
				#'category_id':list_category_id,
				'function':self.browse(cr,uid,op_id,context=context).function,
				'email':self.browse(cr,uid,op_id,context=context).email,
				'country_id':self.browse(cr,uid,op_id,context=context).country_id.id,
				'mobile':self.browse(cr,uid,op_id,context=context).mobile,
				'fax':self.browse(cr,uid,op_id,context=context).fax,
				'street':self.browse(cr,uid,op_id,context=context).street,
				'website':self.browse(cr,uid,op_id,context=context).website,
				'code_tva':self.browse(cr,uid,op_id,context=context).code_tva,
				'parent_id':self.browse(cr,uid,op_id,context=context).parent_id.id,
				'phone':self.browse(cr,uid,op_id,context=context).phone,
				'city':self.browse(cr,uid,op_id,context=context).city,
				'street2':self.browse(cr,uid,op_id,context=context).street2,
				'title':self.browse(cr,uid,op_id,context=context).title.id,
				'vat' : self.browse(cr,uid,op_id,context=context).matricule_fiscale,
				'use_parent_address' : self.browse(cr,uid,op_id,context=context).use_parent_address,
				'registre': self.browse(cr,uid,op_id,context=context).code_tva,
			}
		self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)
		#test if existe ou nn
		#here 19-10-2017
		list_categ =[]
		partner=self.pool.get('res.partner').search(cr,uid,[('name','=',self.browse(cr,uid,op_id,context=context).name)],context=context)

		if  not partner:
			partner_id=self.pool.get('res.partner').create(cr, uid, val, context=context)

			#26-10-2017 AJOUTER LA liste des secteurs
			for categ in self.browse(cr, uid, op_id, context=context).category_id:

				#cr.execute("SELECT category_id FROM res_partner_res_partner_category_rel WHERE partner_id =%s",(partner_id,))
				#lines = cr.dictfetchall()
				#for line in lines :
					#category_id= line['category_id']
				#cr.execute("DELETE FROM res_partner_res_partner_category_rel WHERE category_id =%s AND partner_id =%s",(categ.id,op_id))
				cr.execute("INSERT INTO res_partner_res_partner_category_rel (partner_id , category_id) VALUES (%s, %s)",(partner_id, categ.id))

		else:
			existe_id=self.pool.get('res.partner').write(cr, uid, partner, val,context=context)
			for categ in self.browse(cr, uid, op_id, context=context).category_id:


				cr.execute("SELECT category_id FROM res_partner_res_partner_category_rel WHERE partner_id =%s",(tuple(partner),))
				lines = cr.dictfetchall()
				if lines:

					for line in lines :
						category_id= line['category_id']

						cr.execute("DELETE FROM res_partner_res_partner_category_rel WHERE category_id =%s AND partner_id =%s",(category_id,tuple(partner)))
						list_categ.append(category_id)


			####else
			for categ in self.browse(cr, uid, op_id, context=context).category_id:

				if categ.id not in list_categ:
					list_categ.append(categ.id)

			for ls_categ in list_categ:

				#cr.execute("SELECT category_id FROM res_partner_res_partner_category_rel WHERE partner_id =%s",(tuple(partner),))
				#lines = cr.dictfetchall()
				#if not lines:
					#print 'else ======'
				cr.execute("INSERT INTO res_partner_res_partner_category_rel (partner_id , category_id) VALUES (%s, %s)",(tuple(partner), ls_categ))
					

		return self.write(cr, uid, ids, {'state': 'validate'})
    	 

	def to_reject(self, cr, uid, ids, context=None):
		#notif Responsable
		op_id=self.browse(cr, uid, ids, context=context).id
		create_id=self.browse(cr, uid, op_id, context=context).create_uid.id

		vals = {
			'record_name': "Refus d'une demande d'ajout d'un opérateur économique",
			'body':"<html> L'opérateur économique a été refusé</html>",

			'res_id':op_id,
			'reply_to':uid,
			'author_id':uid,
			'model':'res.partner.request',
			'type':'email',
			'email_from':uid,
			'starred':False,
		}


		mail_notif_vals = {
			'partner_id':self.pool.get('res.users').browse(cr, uid, create_id, context=context).partner_id.id,
			'message_id':self.pool.get('mail.message').create(cr, uid, vals, context=context),
			'is_read':False,
			'starred':False,

		}
		self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)
		return self.write(cr, uid, ids, {'state': 'reject'})

	def to_update(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'state': 'update'})

	#add by marwa BM 02-10-2017	
	def message_redirect_action(self, cr, uid, context=None):
		""" For a given message, return an action that either
		- opens the form view of the related document if model, res_id, and
		  read access to the document
		- opens the Inbox with a default search on the conversation if model,
		  res_id
		- opens the Inbox with context propagated

		"""
		if context is None:
			context = {}
		#super(subClass, instance).method(args)
		return self.pool.get('mail.thread').message_redirect_action(cr, uid, context=context)


	def draft(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'state': 'draft'}, context=context)


	@api.one
	def to_search(self):
		oe_ids = self.env['res.partner'].search([])

		for oe_id in oe_ids:
			name_oe_id = self.env['res.partner'].browse(oe_id.id).name
			val = distance.get_jaro_distance(name_oe_id, self.name, winkler=False, scaling=0.1)
			if val > 0.9:

				vals = {
					'operator_id': oe_id.id,
					'partner_id': self.id,
					'distance': val,  # give id of first
				}

				create_id = self.env['op.eco.distance'].create(vals)


