# -*- coding: utf-8 -*-

from openerp import models, fields, api

class op_eco_distance(models.Model):
    _name="op.eco.distance"

   	#dist =fields.Char(string="distance")

    distance =fields.Float(string='Distance')
    operator_id = fields.Many2one('res.partner',string='Opérateur économique' )
    partner_request_id = fields.Many2one('res.partner.request',string='Demande ajout op eco' )
    	#distance_ids = fields.One2many(comodel_name="res.partner.request", string='Distance', inverse_name="distance")

############ méthode pour chercher les op Eco similaires



