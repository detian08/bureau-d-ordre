# -*- coding: utf-8 -*-
from openerp.tools.translate import _
from openerp.osv import fields, osv
from openerp.exceptions import Warning
from datetime import datetime, date


class product_catgory(osv.osv):
	_name = 'product.category'
	_inherit = 'product.category'
	_columns = {
		'codif_infocham': fields.integer('Code infocham'),
		'attributes_ids': fields.many2many('product.attribute', string="Attributs"),
	}


class product_product(osv.osv):
	_name = 'product.product'
	_inherit = 'product.product'


class product_template(osv.osv):
	_name = 'product.template'
	_inherit = 'product.template'

	_columns = {

	'state': fields.selection(
	[
		('draft', 'Brouillon'),
		('to_validate', 'En cours de validation'),
		('validate', 'Validée'),
	], 'Status', help="Gives the status of the product.", select=True),

	# update by marwa 13-10-2017
	'date_debut': fields.date("Date début", required=True),
	'date_fin': fields.date("Date fin", required=True),
	'product_sector_ids': fields.many2many('res.partner.category', help="Gives all the sector of product.",
									   string="Secteurs d'activité"),

	'ope_eco_ids': fields.one2many('product.participant', 'product_id', 'Operateurs Economiques'),
	'participant_ids': fields.one2many('participant.contact', 'product_id', 'Participants'),
	'session_ids': fields.one2many('product.session', 'product_id', 'Programme'),

	'presence_ids': fields.one2many('session.presence', 'product_id', 'Présence par session'),

	'visite_ids': fields.one2many('product.visite', 'product_id', 'Plan visite'),
	'type': fields.selection([('autres', 'Autres'),('adhesion', 'Adhésion'),('formation', 'Formation'),('visite', 'Visite'), ('foire-mnifest', 'Foire et manifestation')], 'Product Type', required=True, help="Consumable are product where you don't manage stock, a service is a non-material product provided by a company or an individual."),

	#'type_product': fields.many2one('product.type', 'Type Product', required = True),
	'a_suivre':fields.boolean(string="À suivre"),
	}
		
	_defaults = {
		'state': 'draft',
		'type':'foire-mnifest',
	}

	def draft(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'state': 'draft'})

	def to_validate(self, cr, uid, ids, context=None):
		create_uid = self.browse(cr,uid,ids[0],context=context).create_uid.id
		user_name = self.pool.get('res.users').browse(cr, uid, create_uid, context=context).name
		user_email = self.pool.get('res.users').browse(cr, uid, create_uid, context=context).email
		mail_vals = {
			'record_name': "Validation d'une demande d'ajout d'un produit",
			'body': "<html>Un produit a été validé</html>",
			'res_id': ids[0],
			'reply_to': user_name,
			'author_id': uid,
			'model': 'product.template',
			'type': 'email',
			'email_from': user_email,
			 'starred': False,
		}
		message = self.pool.get('mail.message').create(cr, uid, mail_vals)
		mail_notif_vals = {
			'partner_id': self.pool.get('res.users').browse(cr, uid, create_uid, context=context).partner_id.id,
			'message_id': message,
			'is_read': False,
			'starred': False,
		}
		self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)
		return self.write(cr, uid, ids, {'state': 'validate'})

	def draft_to_validate(self, cr, uid, ids, context=None):
		section_ids = self.pool.get('crm.case.section').search(cr, uid, [('code', '=', 'DG')], context=context)
		user_id = self.pool.get('crm.case.section').browse(cr, uid, section_ids, context=context).user_id.id
		user_name = self.pool.get('res.users').browse(cr, uid, user_id, context=context).name
		user_email = self.pool.get('res.users').browse(cr, uid, user_id, context=context).email

		mail_vals = {
			'record_name': "Validation d'un produit",
			'body': "<html>Merci de valider le produit</html>",
			'res_id': ids[0],
			'reply_to': user_name,
			'author_id': uid,
			'model': 'product.template',
			'type': 'notification',
			'email_from': user_email,
			'starred': True,
		}
		message = self.pool.get('mail.message').create(cr, uid, mail_vals)
		mail_notif_vals = {
			'partner_id': self.pool.get('res.users').browse(cr, uid, user_id, context=context).partner_id.id,
			'message_id': message,
			'is_read': False,
			'starred': True,
		}
		notif = self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)
		return self.write(cr, uid, ids, {'state': 'to_validate'})

	def add_attribute(self, cr, uid, ids, context=None):
		# recupérer l'objet en cours
		product_obj = self.browse(cr, uid, ids)

		categ_type = product_obj.categ_id

		attributes_categ = product_obj.attribute_line_ids

		product_line = self.pool.get('product.attribute.line')

		product_tmp = self.browse(cr, uid, ids, context=context)[0]

		attributes_list = categ_type.attributes_ids
		if attributes_list:
			for att in attributes_list:
				values = {
					'product_tmpl_id': product_obj.id,
					'attribute_id': att.id,
				}
				product_line.create(cr, uid, values)

		else:
			pass

		## ***********Plan visite**************


class product_visite(osv.osv):
	_name = 'product.visite'
	_columns = {
		'product_id': fields.many2one('product.template', 'Product_ref', cascade="delete", required=True),
		'date': fields.date("Date du visite", required=True),
		'heure_deb': fields.datetime("Heure début", required=True),
		'heure_fin': fields.datetime("Heure fin", required=True),
		'op_eco': fields.many2one('res.partner', 'id', required=True),
		'note': fields.text("Note"),
	}
	_defaults = {
		'product_id': lambda self, cr, uid, context: context.get('product_id', False),
	}

## ***********Operateur Economique**************


class product_participant(osv.osv):
	_name = 'product.participant'
	_columns = {
		'name': fields.many2one('res.partner', "Operateur Economique", select=True),
		'presence': fields.boolean(string="Presence"),
		'product_id': fields.many2one('product.template', 'Product_ref', cascade="delete"),
	}
	_defaults = {
		'product_id': lambda self, cr, uid, context: context.get('product_id', False),
	}

	def download_contact(self, cr, uid, ids, context=None):
		return {
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'cci.contact.wizard',
			'view_id ref="wizard_form_view_contact"': True,
			'type': 'ir.actions.act_window',
			'target': 'new',
		}

	# def create_participant(self, cr, uid, ids, context=None):


## ***********Participant contact**************
class participant_contact(osv.osv):
	_name = 'participant.contact'

	def get_operateurEco(self, cr, uid, ids, context=None):
		if self.participant_id:
			return self.participant_id.name
		else:
			return False

	_columns = {
		'name': fields.many2one('res.partner', 'Contact', ),  # domain=[('parent_id', '=', get_operateurEco)]),
		'participant_id': fields.many2one('product.participant', 'Operateur Economique', cascade="delete"),
		'presence': fields.boolean(string="Presence"),
		'product_id': fields.many2one('product.template', 'Product_ref', cascade="delete"),
	}
	_defaults = {
		'product_id': lambda self, cr, uid, context: context.get('product_id', False),
	}

	def onchange_participant_id(self, cr, uid, ids, participant_id, context=None):
		res = {}
		if participant_id:
			name = self.pool.get('product.participant').browse(cr, uid, participant_id, context=context).name.id
			res['domain'] = {'name': [('parent_id', '=', name)]}
			return res


## ***********Sessions formation**************
class product_session(osv.osv):
	_name = 'product.session'
	_columns = {
		'name': fields.char('Titre', size=500, required=True, select=True),
		'heure_debut': fields.datetime('Date debut'),
		'heure_fin': fields.datetime('Date fin'),
		'product_id': fields.many2one('product.template', 'Product', cascade="delete"),

	}
	_defaults = {
		'product_id': lambda self, cr, uid, context: context.get('product_id', False),
	}


## ***********Presence session**************
class session_presence(osv.osv):
	_name = 'session.presence'

	_columns = {

		'contact_id': fields.many2one('participant.contact', 'Participant'),
		'session_id': fields.many2one('product.session', 'Session'),
		'presence': fields.boolean(string="Presence"),
		'product_id': fields.many2one('product.template', 'Product_ref'),
	}
	_defaults = {
		'product_id': lambda self, cr, uid, context: context.get('product_id', False),
	}
## ***********type_product**************

