# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime,date

class oe_mining(osv.osv_memory):
    _name = "cci.wizard.oe.mining"

    _columns = {
        'product_id':fields.many2one('product.template', 'Produits', required=True),
        'survey_ids': fields.many2many('survey.survey'),
        'consultation_ids': fields.many2many('cci.consultation', 'cci_wizard_oe_mining_consultation_rel', 'wizard_id','consultation_id'),
	'tags_id': fields.text('Tags'),

        #'consultation_ids': fields.one2many('cci.wizard.oe.mining', 'consult_id', 'Consultations_wizard')
        #'survey_ids': fields.one2many('survey.survey', 'survey_id', 'Sondages_wizard')


#'membres_ids': fields.many2many('res.users', 'res_user_compagne_rel', 'compagne_id', 'user_id', "Membres de l'équipe"),


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


	print 'datas.....',datas
        return {'type': 'ir.actions.report.xml', 'report_name': 'jasper_oe_minig_print', 'datas': datas}


oe_mining()




