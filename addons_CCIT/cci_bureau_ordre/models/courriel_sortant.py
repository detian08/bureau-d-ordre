# -*- coding: utf-8 -*-

from openerp import models, fields, api

class cci_courriel_sortant(models.Model):
	_name = 'cci.courriel.sortant'
	_description="Les courriels sortants"
	_inherit="cci.courriel" 

	reference = fields.Char(string="Réference",readonly=True, default=lambda self:self.env['ir.sequence'].get('RefCourrielSortant'))


	state = fields.Selection([
	('draft', "Brouillon"),
	('to_soumdg', "Soumis à la DG"),
	('to_soumpre', "Soumis au président"),
	#('to_assistantpre', "Soumis au vice-président"),
	('to_conseiller', "Soumis au conseiller"),
	('traite', "Traiter"),
	], default='draft', string="État")
	is_presedent = fields.Boolean(compute="_check_user_group", string="present", store='False')  

#################"function compute


	@api.multi
	def _check_user_group(self):
		uid = self.env.user.id
		section_ids = self.env['crm.case.section'].search([('code', '=', 'BE')])
		user_id = self.env['crm.case.section'].browse(section_ids.id).user_id.id

		
		hr_id = self.env['hr.employee'].search([('user_id', '=', user_id)]).id
		present = self.env['hr.employee'].browse(hr_id).present
		print 'hello compute',present
		if present == True :
			self.is_presedent = True

	@api.multi
	def draft(self):
		print 'hello brouillon'
		self.state = 'draft'
	@api.one
	def to_soumdg(self):
		uid = self.env.user.id
		#uid_email = self.env['res.users'].browse(uid).email
		section_ids = self.env['crm.case.section'].search([('code', '=', 'DG')])
		print 'section_ids....',section_ids
		user_id = self.env['crm.case.section'].browse(section_ids.id).user_id.id
		print 'user_id....',user_id
		user_name = self.env['res.users'].browse(user_id).name
		print 'user_name....',user_name
		mail_vals = {
			'body': '<html>Merci de traiter un courriel sortant soumis.</html>',
			'record_name': "Traitement d'un courriel sortant",
			'res_id': self.id,
			'reply_to': user_name,##dest
			'author_id': uid,#utilisateur en cours##exp
			#'email_from': uid_email,##exp
			'model': 'cci.courriel.sortant',
			'type': 'notification',

			'starred': True,
		}

		#mesg = self.env['mail.message'].create(mail_vals)
		#print 'mesg....',mesg
		mail_notif_vals = {
			'partner_id': self.env['res.users'].browse(user_id).partner_id.id,
			#'message_id': mesg.id,
			'is_read': False,
			'starred': True,
		}
		#notif = self.env['mail.notification'].create(mail_notif_vals)
		self.state = 'to_soumdg'


	@api.one
	def to_soumpre(self):
		print 'hello soumpre'



		uid = self.env.user.id
		section_ids = self.env['crm.case.section'].search([('code', '=', 'BE')])
		user_id = self.env['crm.case.section'].browse(section_ids.id).user_id.id
		hr_id = self.env['hr.employee'].search([('user_id', '=', user_id)]).id
		present = self.env['hr.employee'].browse(hr_id).present
		if present == True :

			user_name = self.env['res.users'].browse(user_id).name
			print 'user_name....',user_name
			user_email = self.env['res.users'].browse(uid).email
			print 'user_email....',user_email
			mail_vals = {
				'body': '<html>Merci de traiter un courriel sortant soumis.</html>',
				'record_name': "Traitement d'un courriel sortant",
				'res_id': self.id,
				'reply_to': user_name,
				'author_id': uid,
				'model': 'cci.courriel.sortant',
				'type': 'notification',
				'email_from': user_email,
				'starred': True,
			}
			mesg = self.env['mail.message'].create(mail_vals)
			print 'mesg....',mesg
			mail_notif_vals = {
				'partner_id': self.env['res.users'].browse(user_id).partner_id.id,
				'message_id': mesg.id,
				'is_read': False,
				'starred': True,
			}
			notif = self.env['mail.notification'].create(mail_notif_vals)
			#return self.write({'state': 'to_soumpre'})
			self.state = 'to_soumpre'


##################"


                elif present==False:   

		        uid = self.env.user.id
		        groups_ids = self.env['res.groups'].search([('name', '=', 'vice président')]).id


		        self.env.cr.execute('SELECT uid FROM res_groups_users_rel WHERE gid = %s',(groups_ids,))
		        group_uid_list = self.env.cr.fetchall()
			print 'group_uid_list....',group_uid_list

		        for group_id in group_uid_list:
				print group_id


		        user_id = self.env['res.users'].browse(group_id).id

			print 'user_id....',user_id
		        group_id = self.env['hr.employee'].search([('user_id', '=', user_id)]).id
			print 'group_id....',group_id
		        #present = self.env['hr.employee'].browse(group_id).present
			#user_name = self.env['res.groups'].browse(user_id).name
			#print 'user_name....',user_name
			user_email = self.env['res.users'].browse(uid).email
			print 'user_email....',user_email
			mail_vals = {
				'body': '<html>Merci de traiter un courriel sortant soumis.</html>',
				'record_name': "Traitement d'un courriel sortant",
				'res_id': self.id,
				#'reply_to': user_name,
				'author_id': uid,
				'model': 'cci.courriel.sortant',
				'type': 'notification',
				'email_from': user_email,
				'starred': True,
			}
			mesg = self.env['mail.message'].create(mail_vals)
			print 'mesg....',mesg
			mail_notif_vals = {
				'partner_id': self.env['res.users'].browse(user_id).partner_id.id,
				'message_id': mesg.id,
				'is_read': False,
				'starred': True,
			}
			notif = self.env['mail.notification'].create(mail_notif_vals)
			self.state = 'to_soumpre'





	#@api.multi
	#def to_assistantpre(self):
		#print "hello Soumis à l'assistant du président"
		#self.state = 'to_assistantpre'





	@api.multi
	def traite(self):
		uid = self.env.user.id
####traiter#####
		uid_email = self.env['res.users'].browse(uid).email
		print 'user email',uid_email

		traiter_ids = self.env['cci.courriel.sortant'].browse(self.id).dept_id.id
		user_name = self.env['res.users'].browse(traiter_ids).name
		print 'user_name....',user_name
		mail_vals = {
			'body': '<html>Merci de traiter un courriel sortant soumis.</html>',
			'record_name': "Traitement d'un courriel sortant",
			'res_id': self.id,
			'reply_to': user_name,
			'author_id': uid,
			'model': 'cci.courriel.sortant',
			'type': 'notification',
			'email_from': uid_email,
			'starred': True,
		}

		mesg = self.env['mail.message'].create(mail_vals)
		print 'mesg....',mesg
		mail_notif_vals = {
			'partner_id': self.env['res.users'].browse(traiter_ids).partner_id.id,
			'message_id': mesg.id,
			'is_read': False,
			'starred': True,
		}
		notif = self.env['mail.notification'].create(mail_notif_vals)
		self.state = 'traite'





	@api.multi
	def to_conseiller(self):
		print 'hello conseiller'
		uid = self.env.user.id
#####Notification conseiller####

		uid_email = self.env['res.users'].browse(uid).email

		conseiller_ids = self.env['cci.courriel.sortant'].browse(self.id).dept_id.id
		print 'conseiller_ids....',conseiller_ids
		user_name = self.env['res.users'].browse(conseiller_ids).name
		print 'user_name....',user_name
		mail_vals = {
			'body': '<html>Merci de traiter un courriel sortant soumis.</html>',
			'record_name': "Traitement d'un courriel sortant",
			'res_id': self.id,
			'reply_to': user_name,
			'author_id': uid,
			'model': 'cci.courriel.sortant',
			'type': 'notification',
			'email_from': uid_email,
			'starred': True,
		}

		mesg = self.env['mail.message'].create(mail_vals)
		print 'mesg....',mesg
		mail_notif_vals = {
			'partner_id': self.env['res.users'].browse(conseiller_ids).partner_id.id,
			'message_id': mesg.id,
			'is_read': False,
			'starred': True,
		}
		notif = self.env['mail.notification'].create(mail_notif_vals)
		self.state = 'to_conseiller'


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
		action=self.pool.get('mail.thread').message_redirect_action(cr, uid, context=context)
		return action



  



