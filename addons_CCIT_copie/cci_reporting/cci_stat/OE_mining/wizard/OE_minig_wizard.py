# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime,date

class oe_mining(osv.osv_memory):
    _name = "cci.wizard.oe.mining"

    _columns = {
        'product_id':fields.many2one('product.template', 'Produit', required=True),
	#'consultation_id':fields.many2one('cci.consultation',r, 'Consultation', required=True),



        'consultation_ids': fields.one2many('cci.consultation', 'type_id', 'Consultations'),
        #'survey_ids': fields.one2many('survey.survey', 'survey_id', 'Sondages'),

    }


    def create_report(self, cr, uid, ids, context=None):
        datas = {}
        if context is None:
            context = {}
        data = self.read(cr, uid, ids)[0]
        datas = {
            'ids': [],
            'model': 'product.template',
            'form': data
        }
        #return {'type': 'ir.actions.report.xml', 'report_name': 'jasper_oe_mining_print', 'datas': datas}


oe_mining()


