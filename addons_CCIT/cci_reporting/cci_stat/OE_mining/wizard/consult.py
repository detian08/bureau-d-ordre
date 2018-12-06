
# -*- coding: utf-8 -*-
from openerp import models, fields, api

class cci_consultation_minig(models.Model):
	_inherit = 'cci.consultation'


	mining_id = fields.Many2one('cci.wizard.oe.mining', 'Mining' , required=True)




