# -*- coding: utf-8 -*-

from openerp import models, fields, api

class cci_consultation(models.Model):
	_name = 'cci.consultation'
	name =fields.Char(string="Réference",readonly=True, default=lambda self:self.env['ir.sequence'].get('RefConsult'))
	type_id = fields.Many2one('cci.type.consultation', 'Type de consultation' , required=True)
	date_cons = fields.Date(string='Date', default=fields.Date.today(), )

	op_eco_exist = fields.Boolean(string="Opérateur Économique Existant", )



	degre = fields.Selection([
	('public', "Public"),
	('prive', "Prive")
	], default='public')

	
	user_ids = fields.Many2many(string="User", comodel_name="res.users", relation="consult_user_rel", column1="consult_id", column2="user_id")
	#groups_id = fields.Many2many(string="Groupe", comodel_name="res.groups", relation="consult_group_rel", column1="consult_id", column2="group_id")



	op_eco_id = fields.Many2one(comodel_name="res.partner", string="Opérateur Économique", )

	op_eco_new = fields.Char(string="Nouvel Opérateur Économique", )

	mobile = fields.Char(string="Tél. portable", )
	mail = fields.Char(string="E-mail", )
	fax = fields.Char(string="Fax", )
	street= fields.Char(string='Rue', select=True)
	phone = fields.Char(string='Tél.')
	street2 = fields.Char(string='Street2')
	zip = fields.Char(string='Code postale', size=24, change_default=True)
	city = fields.Char(string='Ville')
	country_id = fields.Many2one('res.country', string='Pays', ondelete='restrict')
	note =fields.Text(string="Note",)
	responsable = fields.Many2one('res.users', 'Responsable', default=lambda self: self.env.user)
	consult_tag = fields.Many2many(string="Tags", comodel_name="cci.consultation.tags", relation="consult_tag_rel", column1="consult_id", column2="tag_id")




	@api.model
	def create(self, vals):
		print vals

		dg_id = self.env['res.groups'].search([('name', '=', 'DG')]).id
		print 'dg_ids .......',dg_id
		self.env.cr.execute('SELECT uid FROM res_groups_users_rel WHERE gid = %s',(dg_id,))
		dg_uid_list = self.env.cr.fetchall()

		for dg_uid in dg_uid_list:
			print dg_uid

		pre_id =  self.env['res.groups'].search([('name', '=', 'Président')]).id
		self.env.cr.execute('SELECT uid FROM res_groups_users_rel WHERE gid = %s',(pre_id,))
		pre_uid_list = self.env.cr.fetchall()

		for pre_uid in pre_uid_list:
			print pre_uid

		responsable= vals.get('responsable')


		self.env.cr.execute('SELECT section_id FROM sale_member_rel WHERE member_id = %s',(responsable,))
		section_id_list = self.env.cr.fetchall()
		print section_id_list

		for section_id in section_id_list:
			print section_id
		chef_ids = self.env['crm.case.section'].browse(section_id).user_id.id
		print 'chef_ids .......',chef_ids
		if chef_ids :


			vals = {'city': vals.get('city'), 
				'fax': vals.get('fax'), 
				'op_eco_exist': vals.get('op_eco_exist'), 
				'street': vals.get('street'), 
				'date_cons': vals.get('date_cons'), 
				'zip': vals.get('zip'), 
				'type_id': vals.get('type_id'), 
				'mobile': vals.get('mobile'), 
				'street2': vals.get('street2'),
				'country_id': vals.get('country_id'), 
				'degre': vals.get('degre'), 
				'op_eco_new': vals.get('op_eco_new'),
				'note':vals.get('note'),
				'phone': vals.get('phone'),
				'consult_tag': vals.get('consult_tag'), 
				'responsable': vals.get('responsable'),
				'mail': vals.get('mail'),
				'op_eco_id': vals.get('op_eco_id'),
				'user_ids':[(6, 0, [dg_uid,pre_uid,chef_ids])],
				}
	      		return super(cci_consultation, self).create(vals)
		else:
			vals = {'city': vals.get('city'), 
				'fax': vals.get('fax'), 
				'op_eco_exist': vals.get('op_eco_exist'), 
				'street': vals.get('street'), 
				'date_cons': vals.get('date_cons'), 
				'zip': vals.get('zip'), 
				'type_id': vals.get('type_id'), 
				'mobile': vals.get('mobile'), 
				'street2': vals.get('street2'),
				'country_id': vals.get('country_id'), 
				'degre': vals.get('degre'), 
				'op_eco_new': vals.get('op_eco_new'),
				'note':vals.get('note'),
				'phone': vals.get('phone'),
				'consult_tag': vals.get('consult_tag'), 
				'responsable': vals.get('responsable'),
				'mail': vals.get('mail'),
				'op_eco_id': vals.get('op_eco_id'),
				'user_ids':[(6, 0, [dg_uid,pre_uid])],
				}
		
		
	      		return super(cci_consultation, self).create(vals)

		





	#def create (self):
		#"user_ids prend par défaut id du dg et id du président et id du chef du département de l'utilisateur courant(self.env.uid')"

class cci_type_consultation(models.Model):
	_name = 'cci.type.consultation'
	name = fields.Char(string="Type", required=True, )

class cci_consultation_tags(models.Model):
	_name = 'cci.consultation.tags'
	name = fields.Char(string="Tags", )
