# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime,date

class oe_mining(osv.osv_memory):
    _name = "cci.wizard.oe.mining"

    _columns = {


	'critere' : fields.selection([
        ('sondage', "Sondages"),
        ('consultation', "Consultations"),
    ], default='sondage', string="critére"),

    }

    def next_wizard (self,cr,uid,ids,context=None):

	type_critere=self.browse(cr,uid,ids,context=context).critere

	if type_critere =="sondage" :

			return {
			'name': ('Sondages'),
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'cci.next.wizard.survey',
			'view_id ref= survey_form_inherit':True,

			'type': 'ir.actions.act_window',
			'target': 'new',

		}
	if type_critere =="consultation" :

			return {
			'name': ('Consultations'),
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'cci.next.wizard.consultation',
			'view_id ref= consultation_template_form_view':True,

			'type': 'ir.actions.act_window',
			'target': 'new',

		}

	return True

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




