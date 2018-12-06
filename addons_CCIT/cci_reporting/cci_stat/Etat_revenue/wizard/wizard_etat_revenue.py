# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime,date

class wizard_revenue(osv.Model):
    _name = "cci.wizard.revenue"
    _description = "Renenue Wizard"

    _columns = {
        'product_ids': fields.many2many('product.template', 'product_wiz_revenu_rel', 'report_id', 'product_id', 'Produit', required=True),
        #'product_id': fields.many2one('product.template', 'Produit', required=True),
        # 'date':fields.date(string='Année'),
        # 'year': datetime.strptime(str(current_year) + '-01-01', '%Y-%m-%d').date()
        'year':fields.selection([(num, str(num)) for num in range(2000, (datetime.now().year) + 1)], 'Year'),


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
        return {'type': 'ir.actions.report.xml', 'report_name': 'jasper_revenue_print', 'datas': datas}


wizard_revenue()
