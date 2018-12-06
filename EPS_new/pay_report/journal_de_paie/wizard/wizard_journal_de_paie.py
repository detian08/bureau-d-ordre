# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime

class wizard_journal_de_paie(osv.osv_memory):
    _name = "wizard.journal.de.paie"
    _description = " "

    _columns = { 
           
        #'hr_payroll_session_id':fields.many2one('hr.payroll.session', 'Session', required=True,),
        'year': fields.selection([(num, str(num)) for num in range((datetime.now().year)-4, (datetime.now().year)+1 )], 'Année', required=True,),
        'report_type':fields.selection([("pdf","PDF"),
                                        ("xls","Excel"),
                                        ("html","HTML")
                                        ],'Type'),
        
        'state': fields.selection([('choose','choose'),
                                    ('get','get'),
                                   ]),

    }

    def create_report(self, cr, uid, ids, context={}):
        data = self.read(cr,uid,ids,)[-1]
        print data,' create_report('
	res={}
	res={
            'type'         : 'ir.actions.report.xml',
            'report_name'   : 'jasper_report_journal_de_paie_print',
            'datas': {
                    'model':'hr.payslip',
                    'id': context.get('active_ids') and context.get('active_ids')[0] or False,
                    'ids': context.get('active_ids') and context.get('active_ids') or [],
                    'report_type': data['report_type'],
                    'form':data
                    },
            'nodestroy': False
        }
        return res

    _defaults = {
                     'report_type': lambda *a: 'pdf',
                     'state': lambda *a: 'choose',
    }
wizard_journal_de_paie()
