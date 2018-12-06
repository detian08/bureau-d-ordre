# -*- coding: utf-8 -*-
from openerp.tools.translate import _
from openerp.osv import fields, osv
from openerp import api
from openerp.exceptions import Warning
import datetime

class crm_claim(osv.osv):
	_name = 'crm.claim'
	_inherit ='crm.claim'

	def _get_coach_id(self, cr, uid, ids, field_name, arg, context=None):
		res = {}
		for user in self.browse(cr,uid,ids,context=context):
			user_id=self.browse(cr,uid,ids,context=context).user_id.id
			section_ids = self.pool.get('crm.case.section').search(cr, uid, [('member_ids', '=', user_id)], context=context)
			if not section_ids :
				res[user.id] = 0
			else :
				coach_id=self.pool.get('crm.case.section').browse(cr,uid,section_ids[0],context=context).user_id.id
				res[user.id] = coach_id

		return res

	_columns = {
		'name': fields.text('Objet de la réclamation', required=True),
		'product_id' :fields.many2one('product.template', string="Produit", required=True),
		'coach_id': fields.function(_get_coach_id, type="integer"),
		'date_closed': fields.datetime('Closed', readonly=True),
		'history_ids':fields.one2many('crm.claim.history','claim_id','Historique des réclamation'),
		'state': fields.selection(
			[
			('draft', 'Brouillon'),
			('soumise', 'Soumise'),
			('validate', 'Traitée'),
			('reject', 'Rejetée'),
			('close', 'Cloturée'),
			], 'Status', help="Donne l'état de la réclamation.", select=True),
		'note': fields.text('Note'),

	}

	_defaults = {
        	'state': 'draft',
	}

	#@api.model
	#def get_current_user():
	#	print "....get_current_user...."
	#	user_id = self.env['res.users'].browse(self.env.uid).id
	#	return user_id




###############################################
	def validate(self, cr, uid, ids, context=None) :
		user_email = self.pool.get('res.users').browse(cr, uid, uid, context=context).email

		crm_claim_id = self.browse(cr,uid,ids,context=context).id
		responsable = self.browse(cr,uid,crm_claim_id,context=context).user_id.id

		section_id=self.pool.get('crm.case.section').search(cr, uid,[('member_ids','=',responsable)],context=context)

		coach_id=self.pool.get('crm.case.section').browse(cr, uid,section_id,context=context).user_id.id
		#notif Responsable
		mail_vals = {
			'record_name': "Validation d'une réclamation",
			'body':'<html> la réclamation a été validée </html>',
			'res_id':crm_claim_id,
			'reply_to':coach_id,
			'author_id':uid,
			'model':'crm.claim',
			'type':'email',
			'email_from':user_email,
			'starred':False,
		}
		message = self.pool.get('mail.message').create(cr, uid, mail_vals, context=context)
		partner_id=self.pool.get('res.users').browse(cr, uid, coach_id, context=context).partner_id.id
		mail_notif_vals = {
			'partner_id':partner_id,
			'message_id':message,
			'is_read':False,
			'starred':False,

		}
		id_rec=self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)
		partner_name=self.pool.get('res.partner').browse(cr,uid,partner_id).name
		###Créer l'historique
		vals_history = {
			'state':'Traité',
			'partner_id':partner_name,
			'claim_id':crm_claim_id,
			'date_claim':datetime.datetime.now(),
		}
		self.pool.get('crm.claim.history').create(cr, uid,vals_history)
		self.write(cr, uid, ids,{'state':'validate'})

###################################################
	def soumise(self, cr, uid, ids, context=None):
		user_email = self.pool.get('res.users').browse(cr, uid, uid, context=context).email
		crm_claim_id = self.browse(cr,uid,ids,context=context).id
		responsable = self.browse(cr,uid,crm_claim_id,context=context).user_id.id

		#notif Responsable
		mail_vals = {
			'record_name': "Traitement d'une réclamation",
			'body':'<html> Merci de traiter cette réclamation</html>',
			'res_id':crm_claim_id,
			'reply_to':responsable,
			'author_id':uid,
			'model':'crm.claim',
			'type':'notification',
			'email_from':user_email,
			'starred':True,
		}
		message = self.pool.get('mail.message').create(cr, uid, mail_vals, context=context)
		partner_id=self.pool.get('res.users').browse(cr, uid, responsable, context=context).partner_id.id
		mail_notif_vals = {
			'partner_id':partner_id,
			'message_id':message,
			'is_read':False,
			'starred':True,

		}
		id_rec=self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)
		partner_name=self.pool.get('res.partner').browse(cr,uid,partner_id).name
		user_id=self.pool.get('res.users').browse(cr, uid, uid, context=context).partner_id.id
		user_name = self.pool.get('res.partner').browse(cr,uid,user_id).name
		date_claim = self.browse(cr,uid,crm_claim_id,context=context).date
		###Créer l'historique
		vals_draft_history = {
			'state':'Brouillon',
			'partner_id':user_name,
			'claim_id':crm_claim_id,
			'date_claim':date_claim,
		}
		self.pool.get('crm.claim.history').create(cr, uid,vals_draft_history)
		vals_history = {
			'state':'Soumise',
			'partner_id':partner_name,
			'claim_id':crm_claim_id,
			'date_claim':datetime.datetime.now(),
		}
		self.pool.get('crm.claim.history').create(cr, uid,vals_history)
		self.write(cr, uid, ids,{'state':'soumise'})

###################################################
	def close(self, cr, uid, ids, context=None):
		user_email = self.pool.get('res.users').browse(cr, uid, uid, context=context).email
		crm_claim_id = self.browse(cr,uid,ids,context=context).id

		# responsable = self.browse(cr,uid,crm_claim_id,context=context).user_id.id
		#notif Responsable
		create_uid = self.browse(cr,uid,crm_claim_id,context=context).create_uid.id
		mail_vals = {
			'record_name':"Clôture d'une réclamation",
			'body':'<html>La réclamation a été clôturée</html>',
			'res_id':crm_claim_id,
			'reply_to':create_uid,
			'author_id':uid,
			'model':'crm.claim',
			'type':'email',
			'email_from':user_email,
			'starred':False,
		}
		message = self.pool.get('mail.message').create(cr, uid, mail_vals, context=context) 

		partner_id=self.pool.get('res.users').browse(cr, uid, create_uid, context=context).partner_id.id
		mail_notif_vals = {
			'partner_id':partner_id,
			'message_id':message,
			'is_read':False,
			'starred':False,

		}
		id_rec=self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)

		partner_name=self.pool.get('res.partner').browse(cr,uid,partner_id).name
		###Créer l'historique
		vals_history = {
			'state':'Cloturée',
			'partner_id':partner_name,
			'claim_id':crm_claim_id,
			'date_claim':datetime.datetime.now(),
		}
		self.pool.get('crm.claim.history').create(cr, uid,vals_history)

		self.write(cr, uid, ids,{'state':'close'})

#####################################################
	def reject(self, cr, uid, ids, context=None):
		user_email = self.pool.get('res.users').browse(cr, uid, uid, context=context).email

		crm_claim_id = self.browse(cr,uid,ids,context=context).id
		responsable = self.browse(cr,uid,crm_claim_id,context=context).user_id.id
		section_id=self.pool.get('crm.case.section').search(cr, uid,[('member_ids','=',responsable)],context=context)
		coach_id=self.pool.get('crm.case.section').browse(cr, uid,section_id,context=context).user_id.id

#notif Responsable
		mail_vals = {
			'record_name': "Rejet d'une réclamation",
			'body':'<html>La réclamation a été rejetée</html>',

			'res_id':crm_claim_id,
			'reply_to':coach_id,
			'author_id':uid,
			'model':'crm.claim',
			'type':'email',
			'email_from':user_email,
			'starred':False,
		}
		message = self.pool.get('mail.message').create(cr, uid, mail_vals, context=context) 

		partner_id=self.pool.get('res.users').browse(cr, uid, coach_id, context=context).partner_id.id
		mail_notif_vals = {
			'partner_id':partner_id,
			'message_id':message,
			'is_read':False,
			'starred':False,

		}
		id_rec=self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)
		partner_name=self.pool.get('res.partner').browse(cr,uid,partner_id).name
		###Créer l'historique
		vals_history = {
			'state':'Rejetée',
			'partner_id':partner_name,
			'claim_id':crm_claim_id,
			'date_claim':datetime.datetime.now(),
		}
		self.pool.get('crm.claim.history').create(cr, uid,vals_history)
		self.write(cr, uid, ids,{'state':'reject'})


class crm_claim_history(osv.osv):
	_name = 'crm.claim.history'

	_columns = {
		'claim_id':fields.many2one('crm.claim'),
		'state':fields.char('État'),
		'partner_id':fields.char('Partenaire'),
		'date_claim':fields.datetime('Date'),
}



