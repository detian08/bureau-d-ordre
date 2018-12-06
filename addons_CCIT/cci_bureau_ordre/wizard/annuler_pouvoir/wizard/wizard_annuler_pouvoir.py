# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime,date

class annuler_pouvoir(osv.osv_memory):
    _name = "cci.wizard.annuler_pouvoir"

 


    def create_report_oui(self, cr, uid, ids, context=None):
	section_id = self.pool.get('crm.case.section').search(cr, uid, [('code', '=', 'BE')],context=context)
	user_id = self.pool.get('crm.case.section').browse(cr, uid,section_id,context=context).user_id.id
	hr_emp_id=self.pool.get('hr.employee').search(cr, uid, [('user_id', '=', user_id)],context=context)
	return self.pool.get('hr.employee').write(cr,uid,hr_emp_id,{'present': 'True'},context=context)
	


       


    def create_report_non(self, cr, uid, ids, context=None):
	section_id = self.pool.get('crm.case.section').search(cr, uid, [('code', '=', 'BE')],context=context)
	user_id = self.pool.get('crm.case.section').browse(cr, uid,section_id,context=context).user_id.id
	hr_emp_id=self.pool.get('hr.employee').search(cr, uid, [('user_id', '=', user_id)],context=context)
	return self.pool.get('hr.employee').write(cr,uid,hr_emp_id,{'present': 'False'},context=context)




annuler_pouvoir()

