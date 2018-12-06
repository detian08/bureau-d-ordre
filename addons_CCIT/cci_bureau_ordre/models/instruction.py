# -*- coding: utf-8 -*-

from openerp import models, fields, api

class courriel_instruction(models.Model):
	_name = 'courriel.instruction'

	name =fields.Text(string="Instruction")
	dept_id = fields.Many2one('res.users', 'Responsable', default=lambda self: self.env.user )
	#responsable_id = fields.Many2one('res.partner', 'Responsable' , required=True)
	#responsable_id = fields.Many2one('res.users', 'Responsable', default=lambda self: self.env.user)
	date_instruction = fields.Date(string='Date', default=fields.Date.today(), )
	instruction =fields.Text(string="Instruction",)


