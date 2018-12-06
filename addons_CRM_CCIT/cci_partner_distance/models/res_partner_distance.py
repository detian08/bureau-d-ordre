# -*- coding: utf-8 -*-

from openerp import models, fields, api


class res_partner_distance(models.Model):
    _name="res.partner.distance"

    distance =fields.Float(string='Distance')
    operator_id = fields.Many2one('res.partner',string='Opérateur économique' )
    partner_request_id = fields.Many2one('res.partner.request',string='Demande ajout op eco')

