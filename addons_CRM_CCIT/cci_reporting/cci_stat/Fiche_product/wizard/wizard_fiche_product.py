# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime

class wizard_fiche_product(osv.osv_memory):
    _name = "cci.wizard.fiche.product"
    _description = "Fiche product Wizard "

    _columns = {
        'product_id': fields.many2one('product.template', 'Produit', required=True),
        'debut':fields.date('Du'),
        'fin':fields.date("Jusqu'à"),
    }



    def create_report(self, cr, uid, ids, context=None):
        datas = {}
        if context is None:
            context = {}
        data = self.read(cr, uid, ids)[0]
        datas = {
            'ids': [],
            'model': 'object.object',
            'form': data
        }
        return {'type': 'ir.actions.report.xml', 'report_name': 'jasper_fiche_product_print', 'datas': datas}

wizard_fiche_product()
