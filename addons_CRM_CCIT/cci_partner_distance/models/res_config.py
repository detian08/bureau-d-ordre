# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

class jaro_configuration(osv.TransientModel):
    _inherit="sale.config.settings"

    _columns = {
        'seuil': fields.float("Seuil de simmularité"),
    }