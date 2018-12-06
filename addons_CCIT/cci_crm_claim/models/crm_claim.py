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


################################################
    	def draft_to_soumise(self, cr, uid, ids, context=None):
		print '...draft_to_soumise......'
		crm_claim_id = self.browse(cr,uid,ids,context=context).id
		responsable = self.browse(cr,uid,crm_claim_id,context=context).user_id.id

		
		#notif Responsable
		mail_vals = {
			'body':'<html> CCI Liste Des RÉCLAMATIONS </html>',
			'record_name':'Réclamation',
			'res_id':crm_claim_id,
			'reply_to':responsable,
			'author_id':uid,
			'model':'crm.claim',
			'type':'notification',
			'email_from':uid,
			'starred':True,
		}
		message = self.pool.get('mail.message').create(cr, uid, mail_vals, context=context) 

		partner_id=self.pool.get('res.users').browse(cr, uid, responsable, context=context).partner_id.id
		print "..............",partner_id
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
	


###############################################
	def validate(self, cr, uid, ids, context=None) :
		print ".........validate................"
		crm_claim_id = self.browse(cr,uid,ids,context=context).id
		responsable = self.browse(cr,uid,crm_claim_id,context=context).user_id.id
		print "responsable.....",responsable

		section_id=self.pool.get('crm.case.section').search(cr, uid,[('code','=','DG')],context=context)
		print 'section_id........',section_id
		user_id=self.pool.get('crm.case.section').browse(cr, uid,section_id,context=context).user_id.id
		print 'section_id........',section_id
		#section_ids = self.pool.get('crm.case.section').search(cr, uid, [('code', '=', 'DG')], context=context)
		#user_id = self.pool.get('crm.case.section').browse(cr, uid, section_ids, context=context).user_id.id
		user_name = self.pool.get('res.users').browse(cr, uid, user_id, context=context).name
		user_email = self.pool.get('res.users').browse(cr, uid, user_id, context=context).email






		#notif Responsable
##"il faut notifier chef departement DG




		mail_vals = {
			'body':'<html> CCI Liste Des RÉCLAMATIONS </html>',
			'record_name':'Réclamation Test',
			'res_id': ids[0],
			'reply_to': user_name,
			'author_id': user_id,
			'model':'crm.claim',
			'type':'notification',
			'email_from': user_email,
			'starred':True,
		}
		message = self.pool.get('mail.message').create(cr, uid, mail_vals) 

		#partner_id=self.pool.get('res.users').browse(cr, uid, coach_id, context=context).partner_id.id
		print "..............",partner_id
		mail_notif_vals = {
			'partner_id': self.pool.get('res.users').browse(cr, uid, user_id, context=context).partner_id.id,
			'message_id':message,
			'is_read':False,
			'starred':True,

		}
		notif = self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)




		#id_rec=self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)
		partner_name=self.pool.get('res.partner').browse(cr,uid,partner_id).name



		###Créer l'historique
		vals_history = {
			'state':'Traité',
			'partner_id':partner_name,
			'claim_id':crm_claim_id,
			'date_claim':datetime.datetime.now(),
		}
		self.pool.get('crm.claim.history').create(cr, uid,vals_history)
		return self.write(cr, uid, ids,{'state':'validate'})

###################################################
	def soumise(self, cr, uid, ids, context=None):
		print '...........................état soumise'
		##réclamation pour partner_id
		crm_claim_id = self.browse(cr, uid, ids, context=context).id
		user_id = self.browse(cr, uid, crm_claim_id, context=context).user_id.id
		print "responsable.....",user_id

		section_id = self.pool.get('crm.case.section').search(cr, uid, [('member_ids', '=', user_id)],context=context)
		coach_id = self.pool.get('crm.case.section').browse(cr, uid, section_id, context=context).user_id.id

		# notif Responsable
		mail_vals = {
			'body': '<html> CCI Liste Des RÉCLAMATIONS </html>',
			'record_name': 'Réclamation Soumise',
			'res_id': crm_claim_id,
			'reply_to': coach_id,
			'author_id': uid,
			'model': 'crm.claim',
			'type': 'notification',
			'email_from': uid,
			'starred': True,
		}
		message = self.pool.get('mail.message').create(cr, uid, mail_vals, context=context)

		partner_id = self.pool.get('res.users').browse(cr, uid, coach_id, context=context).partner_id.id
		mail_notif_vals = {
			'partner_id': partner_id,
			'message_id': message,
			'is_read': False,
			'starred': True,
		}
		id_rec = self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)
		partner_name = self.pool.get('res.partner').browse(cr, uid, partner_id).name
		###Créer l'historique
		vals_history = {
			'state': 'Soumise',
			'partner_id': partner_name,
			'claim_id': crm_claim_id,
			'date_claim': datetime.datetime.now(),
		}
		self.pool.get('crm.claim.history').create(cr, uid, vals_history)
		return self.write(cr, uid, ids,{'state':'soumise'})
###################################################
	def reject_to_close(self, cr, uid, ids, context=None):
		print '...........................état close'
		##réclamation pour partner_id
		crm_claim_id = self.browse(cr, uid, ids, context=context).id
		user_id = self.browse(cr, uid, crm_claim_id, context=context).user_id.id
		print "responsable.....",user_id

		section_id = self.pool.get('crm.case.section').search(cr, uid, [('member_ids', '=', user_id)],context=context)
		coach_id = self.pool.get('crm.case.section').browse(cr, uid, section_id, context=context).user_id.id

		# notif Responsable
		mail_vals = {
			'body': '<html> CCI Liste Des RÉCLAMATIONS </html>',
			'record_name': 'Réclamation Cloturée',
			'res_id': crm_claim_id,
			'reply_to': coach_id,
			'author_id': uid,
			'model': 'crm.claim',
			'type': 'notification',
			'email_from': uid,
			'starred': True,
		}
		message = self.pool.get('mail.message').create(cr, uid, mail_vals, context=context)

		partner_id = self.pool.get('res.users').browse(cr, uid, coach_id, context=context).partner_id.id
		mail_notif_vals = {
			'partner_id': partner_id,
			'message_id': message,
			'is_read': False,
			'starred': True,
		}
		id_rec = self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)
		partner_name = self.pool.get('res.partner').browse(cr, uid, partner_id).name
		###Créer l'historique
		vals_history = {
			'state': 'Cloturée',
			'partner_id': partner_name,
			'claim_id': crm_claim_id,
			'date_claim': datetime.datetime.now(),
		}
		self.pool.get('crm.claim.history').create(cr, uid, vals_history)
		return self.write(cr, uid, ids,{'state':'close'})
###################################################
	def close_to_soumise(self, cr, uid, ids, context=None):
		print '...........................état soumise'
		##réclamation pour partner_id
		crm_claim_id = self.browse(cr, uid, ids, context=context).id
		user_id = self.browse(cr, uid, crm_claim_id, context=context).user_id.id
		print "responsable.....",user_id

		section_id = self.pool.get('crm.case.section').search(cr, uid, [('member_ids', '=', user_id)],context=context)
		coach_id = self.pool.get('crm.case.section').browse(cr, uid, section_id, context=context).user_id.id

		# notif Responsable
		mail_vals = {
			'body': '<html> CCI Liste Des RÉCLAMATIONS </html>',
			'record_name': 'Réclamation Soumise',
			'res_id': crm_claim_id,
			'reply_to': coach_id,
			'author_id': uid,
			'model': 'crm.claim',
			'type': 'notification',
			'email_from': uid,
			'starred': True,
		}
		message = self.pool.get('mail.message').create(cr, uid, mail_vals, context=context)

		partner_id = self.pool.get('res.users').browse(cr, uid, coach_id, context=context).partner_id.id
		mail_notif_vals = {
			'partner_id': partner_id,
			'message_id': message,
			'is_read': False,
			'starred': True,
		}
		id_rec = self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)
		partner_name = self.pool.get('res.partner').browse(cr, uid, partner_id).name
		###Créer l'historique
		vals_history = {
			'state': 'Soumise',
			'partner_id': partner_name,
			'claim_id': crm_claim_id,
			'date_claim': datetime.datetime.now(),
		}
		self.pool.get('crm.claim.history').create(cr, uid, vals_history)
		return self.write(cr, uid, ids,{'state':'soumise'})
###################################################
	def close(self, cr, uid, ids, context=None):
		crm_claim_id = self.browse(cr,uid,ids,context=context).id
		responsable = self.browse(cr,uid,crm_claim_id,context=context).user_id.id
		create_uid = self.browse(cr,uid,crm_claim_id,context=context).create_uid.id
		partner_id=self.pool.get('res.users').browse(cr, uid, responsable, context=context).partner_id.id

#notif Responsable
		create_uid = self.browse(cr,uid,crm_claim_id,context=context).create_uid.id
		print 'create_uid .....',create_uid
		mail_vals = {
			'body':'<html> CCI Liste Des RÉCLAMATIONS </html>',
			'record_name':'Réclamation Cloturée',
			'res_id':crm_claim_id,
			'reply_to':create_uid,
			'author_id':uid,
			'model':'crm.claim',
			'type':'notification',
			'email_from':uid,
			'starred':True,
		}
		message = self.pool.get('mail.message').create(cr, uid, mail_vals, context=context) 

		partner_id=self.pool.get('res.users').browse(cr, uid, create_uid, context=context).partner_id.id
		print "..............",partner_id
		mail_notif_vals = {
			'partner_id':partner_id,
			'message_id':message,
			'is_read':False,
			'starred':True,

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
		return self.write(cr, uid, ids,{'state':'close'})

#####################################################
#il faut notifier chef département DG
	def reject(self, cr, uid, ids, context=None):
		crm_claim_id = self.browse(cr,uid,ids,context=context).id
		responsable = self.browse(cr,uid,crm_claim_id,context=context).user_id.id
		print "responsable.....",responsable
		#partner_id=self.pool.get('res.users').browse(cr, uid, responsable, context=context).partner_id.id
		#section_id=self.pool.get('crm.case.section').search(cr, uid,[('member_ids','=',responsable)],context=context)
		#print 'section_id........',section_id
		#coach_id=self.pool.get('crm.case.section').browse(cr, uid,section_id,context=context).user_id.id
		#print 'section_id........',section_id

		section_id=self.pool.get('crm.case.section').search(cr, uid,[('code','=','DG')],context=context)
		print 'section_id........',section_id
		user_id=self.pool.get('crm.case.section').browse(cr, uid,section_id,context=context).user_id.id
		print 'section_id........',section_id
		#section_ids = self.pool.get('crm.case.section').search(cr, uid, [('code', '=', 'DG')], context=context)
		#user_id = self.pool.get('crm.case.section').browse(cr, uid, section_ids, context=context).user_id.id
		user_name = self.pool.get('res.users').browse(cr, uid, user_id, context=context).name
		print 'user_name........',user_name
		user_email = self.pool.get('res.users').browse(cr, uid, user_id, context=context).email
		print 'user_email........',user_email





#notif Responsable


		mail_vals = {
			'body':'<html> CCI Liste Des RÉCLAMATIONS </html>',
			'record_name':'Réclamation Rejetée',
			'res_id': ids[0],
			'reply_to': user_name,
			'author_id': user_id,
			'model':'crm.claim',
			'type':'notification',
			'email_from': user_email,
			'starred':True,
		}
		message = self.pool.get('mail.message').create(cr, uid, mail_vals) 

		#partner_id=self.pool.get('res.users').browse(cr, uid, coach_id, context=context).partner_id.id
		#print "..............",partner_id
		mail_notif_vals = {
			'partner_id': self.pool.get('res.users').browse(cr, uid, user_id, context=context).partner_id.id,
			'message_id':message,
			'is_read':False,
			'starred':True,

		}
		notif = self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)



		#id_rec=self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)

		partner_name=self.pool.get('res.partner').browse(cr,uid,partner_id).name
		user_name=self.pool.get('res.partner').browse(cr,uid,user_id).name
		print 'user_name........',user_name
		###Créer l'historique
		vals_history = {
			'state':'Rejetée',
			'partner_id':user_name,
			'claim_id':crm_claim_id,
			'date_claim':datetime.datetime.now(),
		}
		self.pool.get('crm.claim.history').create(cr, uid,vals_history)
		return self.write(cr, uid, ids,{'state':'reject'})


#	def create(self, cr, uid, vals, context=None):
#		crm_claim_id = super(crm_claim, self).create(cr, uid, vals, context=context)
#		dict = vals
#		user_id=dict['user_id']

		#notif Responsable
#		mail_vals = {
#			'body':'<html> CCI Liste Des RÉCLAMATIONS </html>',
#			'record_name':'Réclamation',
#			'res_id':crm_claim_id,
#			'reply_to':user_id,
#			'author_id':uid,
#			'model':'crm.claim',
#			'type':'notification',
#			'email_from':uid,
#			'starred':True,
#		}
#		message = self.pool.get('mail.message').create(cr, uid, mail_vals, context=context) 

#		partner_id=self.pool.get('res.users').browse(cr, uid, user_id, context=context).partner_id.id
#		mail_notif_vals = {
#			'partner_id':partner_id,
#			'message_id':message,
	#		'is_read':False,
	#		'starred':True,

	#	}
	#	id_rec=self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)
	#	return crm_claim_id

    #suite à la changement de l'état de la réclamation, une notification sera envoyé au responsable 
    #@api.multi  
    #@api.onchange('stage_id')  # triggered fields
    #def write(self, vals):
	#super(crm_claim, self).write(vals)
#	if self.stage_id:
#		name = self.env['crm.claim.stage'].browse(self.stage_id.id).name
		
#		mail_vals = {
#			'body':'<html> CCI Liste Des RÉCLAMATIONS </html>',
#			'record_name':'Réclamation',
#			'res_id':self.id,
#			'reply_to':self.user_id,
#			'author_id':self.env.uid,
#			'model':'crm.claim',
#			'type':'notification',
#			'email_from':self.env.uid,
#			'starred':True,
#		}
#		message = self.env['mail.message'].create(mail_vals)
#		partner_id=self.env['res.users'].browse(self.user_id.id).partner_id.id
#		mail_notif_vals = {
#			'partner_id':partner_id,
#			'message_id':message.id,
#			'is_read':False,
#			'starred':True,
#		}
#		self.env['mail.notification'].create(mail_notif_vals)



class crm_claim_history(osv.osv):
	_name = 'crm.claim.history'

	_columns = {
		'claim_id':fields.many2one('crm.claim'),
		'state':fields.char('État'),
		'partner_id':fields.char('Partenaire'),
		'date_claim':fields.datetime('Date'),
}



