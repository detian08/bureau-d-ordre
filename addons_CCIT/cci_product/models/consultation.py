# -*- coding: utf-8 -*-

from openerp import models, fields, api

class cci_consultation(models.Model):
	_name = 'cci.consultation'
	name =fields.Char(string="Réference",readonly=True, default=lambda self:self.env['ir.sequence'].get('RefConsult'))
	type_id = fields.Many2one('cci.type.consultation', 'Type de consultation' , required=True)
	date_cons = fields.Date(string='Date', default=fields.Date.today(), )

	op_eco_exist = fields.Boolean(string="Opérateur Économique Existant", )

	op_eco_id = fields.Many2one(comodel_name="res.partner", string="Opérateur Économique", )
	op_eco_new = fields.Char(string="Nouvel Opérateur Économique", )

	note =fields.Text(string="Note",)
	responsable = fields.Many2one('res.users', 'Responsable', default=lambda self: self.env.user)
	consult_tag = fields.Many2many(string="Tags", comodel_name="cci.consultation.tags", relation="consult_tag_rel", column1="consult_id", column2="tag_id")

    #type_conv_ids = fields.Many2one(comodel_name="type.conventions", string="Professionnel santé", )

class cci_type_consultation(models.Model):
	_name = 'cci.type.consultation'
	name = fields.Char(string="Type", required=True, )

class cci_consultation_tags(models.Model):
	_name = 'cci.consultation.tags'
	name = fields.Char(string="Tags", )