# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime

class wizard_cheque_depense(osv.osv_memory):
    _name = "wizard.cheque.depense"
    _description = "Cheques depenses Wizard "



    # def create_report(self, cr, uid, ids, context={}):
     #    data = self.read(cr,uid,ids,)[-1]
     #    print data,' create_report('
	# res={}
	# res={
     #        'type': 'ir.actions.report.xml',
     #        'report_name'   : 'jasper_cheques_depenses_print',
     #        'datas': {
     #                'model':'office.cheque',
     #                'id': context.get('active_ids') and context.get('active_ids')[0] or False,
     #                'ids': context.get('active_ids') and context.get('active_ids') or [],
     #                'form':data
     #                },
     #        'nodestroy': False
     #    }
     #    return res


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
        return {'type': 'ir.actions.report.xml', 'report_name': 'jasper_cheques_depenses_print', 'datas': datas}

wizard_cheque_depense()
