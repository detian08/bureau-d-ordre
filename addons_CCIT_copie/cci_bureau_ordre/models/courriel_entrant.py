# -*- coding: utf-8 -*-

from openerp import models, fields, api

class cci_courriel_entrant(models.Model):
	_name = 'cci.courriel.entrant'
	_description="Les courriels entrants"
	_inherit="cci.courriel" 

	ref_entrant = fields.Char(string="Réference",readonly=True, default=lambda self:self.env['ir.sequence'].get('RefCourrielEntrant'))
	state = fields.Selection([
		('draft', "Brouillon"),
		('to_soumpre', "Soumis au président"),
		('to_soumdg', "Soumis à la DG"),
		('traite', "Traiter"),
		], default='draft', string="État")

	@api.multi
	def draft(self):
		print 'hello brouillon'
		self.state = 'draft'


	@api.one
	def to_soumpre(self):
		section_ids = self.env['crm.case.section'].search([('code', '=', 'BE')])
		print 'section_ids....',section_ids

		user_id = self.env['crm.case.section'].browse(section_ids.id).user_id.id
		print 'user_id....',user_id
		#user_id = self.dept_id.id
		print 'user_id....',user_id
		user_name = self.env['res.users'].browse(user_id).name
		print 'user_name....',user_name
		user_email = self.env['res.users'].browse(user_id).email
		print 'user_email....',user_email
		mail_vals = {
			'body': '<html>Merci de traiter le couuriel soumis</html>',
			'record_name': 'Courriel entrant',
			'res_id': self.id,
			'reply_to': user_name,
			'author_id': user_id,
			'model': 'cci.courriel.entrant',
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





	@api.one
	def to_soumdg(self):

		section_ids = self.env['crm.case.section'].search([('code', '=', 'DG')])
		print 'section_ids....',section_ids

		user_id = self.env['crm.case.section'].browse(section_ids.id).user_id.id
		print 'user_id....',user_id

		#user_id = self.env['crm.case.section'].browse().user_id.id
		#user_id = self.dept_id.id
		print 'user_id....',user_id
		user_name = self.env['res.users'].browse(user_id).name
		print 'user_name....',user_name
		user_email = self.env['res.users'].browse(user_id).email
		print 'user_email....',user_email
		mail_vals = {
			'body': '<html>Merci de traiter le couuriel soumis</html>',
			'record_name': 'Courriel entrant',
			'res_id': self.id,
			'reply_to': user_name,
			'author_id': user_id,
			'model': 'cci.courriel.entrant',
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
		self.state = 'to_soumdg'


	@api.multi
	def traite(self):
		print 'hello traite'
		self.state = 'traite'








  



