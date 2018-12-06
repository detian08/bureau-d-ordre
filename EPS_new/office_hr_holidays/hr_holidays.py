# -*- coding: utf-8 -*-
##################################################################################
#
# Copyright (c) 2005-2006 Axelor SARL. (http://www.axelor.com)
# and 2004-2010 Tiny SPRL (<http://tiny.be>).
#
# $Id: hr.py 4656 2006-11-24 09:58:42Z Cyp $
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import datetime
import math
import time
from datetime import datetime
from datetime import date
from operator import attrgetter

from openerp.exceptions import Warning
from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _

class hr_holidays_status(osv.osv):
    _inherit = "hr.holidays.status"
    _columns = {
    	'active': fields.boolean('Active', help="If the active field is set to false, it will allow you to hide the leave type without removing it."),
    
    
    }

    _defaults = {
    	'active': False,
    	
	
        
    }      #
    



class hr_holidays(osv.osv):
    _name = "hr.holidays"

    _inherit = ['hr.holidays', 'mail.thread']
    _columns = {




	}
	
    def check_holidays(self, cr, uid, ids, context=None):
        for record in self.browse(cr, uid, ids, context=context):
            if record.holiday_type != 'employee' or record.type != 'remove' or not record.employee_id or record.holiday_status_id.limit:
                continue
            leave_days = self.pool.get('hr.holidays.status').get_days(cr, uid, [record.holiday_status_id.id], record.employee_id.id, context=context)[record.holiday_status_id.id]
            #if leave_days['remaining_leaves'] < 0 or leave_days['virtual_remaining_leaves'] < 0:
                # Raising a warning gives a more user-friendly feedback than the default constraint error
                #raise Warning(_('The number of remaining leaves is not sufficient for this leave type.\n'
                                #'Please verify also the leaves waiting for validation.'))
        return True

    def holidays_validate(self, cr, uid, ids, context=None):
    
    

		validate = super(hr_holidays, self).holidays_validate(cr, uid, ids, context=context)

		if validate:

			obj=self.browse(cr, uid,ids)

			mail_vals = {
					'body':'<html>Votre demande de congé a été acceptée </html>',
					'record_name':'demande congé approuvée',
					'res_id':ids[0],
					'reply_to':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
					'author_id':self.pool.get('res.users').browse(cr, uid, uid, context=context).partner_id.id,
					'model':'hr.holidays',
					'type':'comment',
					'email_from':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
					'starred':True,
			}
			message = self.pool.get('mail.message').create(cr, uid, mail_vals) 

					
			mail_notif_vals = {
					'partner_id':self.pool.get('res.users').browse(cr, uid,obj.employee_id.user_id.id, context=context).partner_id.id,
					'message_id':message,
					'is_read':False,
					'starred':True,
						
			}
			self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)

		return validate



    def holidays_refuse(self, cr, uid, ids, context=None):

		refuse = super(hr_holidays, self).holidays_refuse(cr, uid, ids, context=context)

		if refuse:
			obj=self.browse(cr, uid,ids)

			mail_vals = {
					'body':'<html>Votre demande de congé a été refusée </html>',
					'record_name':'demande congé refusée',
					'res_id':ids[0],
					'reply_to':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
					'author_id':self.pool.get('res.users').browse(cr, uid, uid, context=context).partner_id.id,
					'model':'hr.holidays',
					'type':'comment',
					'email_from':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
					'starred':True,
			}
			message = self.pool.get('mail.message').create(cr, uid, mail_vals)  
					
			mail_notif_vals = {
					'partner_id':self.pool.get('res.users').browse(cr, uid,obj.employee_id.user_id.id, context=context).partner_id.id,
					'message_id':message,
					'is_read':False,
					'starred':True,
						
			}
			self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)
		return refuse



    def create(self, cr, uid, values, context=None):
	
	
        
		##notifier resposanble

        
        
        	
		name_categ='Human Resources'
		hr_holiday_id = super(hr_holidays, self).create(cr, uid, values, context=context)
		name = values.get('name', False)
		cr.execute('SELECT id FROM ir_module_category WHERE name= %s ', (name_categ,))
		rec=cr.dictfetchone()
		categ_id=rec['id']
		name_grp='Manager'
		cr.execute('SELECT id FROM res_groups WHERE name= %s AND category_id=%s ', (name_grp,categ_id,))
		rec=cr.dictfetchone()
		gpg_id=rec['id']
		cr.execute('SELECT id FROM res_users,res_groups_users_rel WHERE res_users.id = res_groups_users_rel.uid AND res_users.active = True AND res_groups_users_rel.gid =%s ', (gpg_id,))
		record=cr.dictfetchall()
		if len(record) > 0 and hr_holiday_id:
			for user in record:
				user_id=user['id']
          

				mail_vals = {
					'body':'<html>Vous avez une demande de congé </html>',
					'record_name':'demande congé ',
					'res_id':hr_holiday_id,
					'reply_to':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
					'author_id':self.pool.get('res.users').browse(cr, uid, uid, context=context).partner_id.id,
					'model':'hr.holidays',
					'type':'comment',
					'email_from':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
					'starred':True,
				}
				message = self.pool.get('mail.message').create(cr, uid, mail_vals) 

					
				mail_notif_vals = {
					'partner_id':self.pool.get('res.users').browse(cr, uid,user_id, context=context).partner_id.id,
					'message_id':message,
					'is_read':False,
					'starred':True,
						
				}
				self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)

		return hr_holiday_id	

#########14-03-2018 action planifié

class hr_employee(osv.osv):
    _inherit = "hr.employee"
    _columns = {
	'jr_cong_ann': fields.float('Jours de congé annuel'),
 	#'remaining_leaves': fields.function(_get_remaining_days, string='Remaining Legal Leaves', fnct_inv=_set_remaining_days, type="float", help='Total number of legal leaves allocated to this employee, change this value to create allocation/leave request. Total based on all the leave types without overriding limit.', store=True),
    }

    def alimenter_conge(self, cr, uid, context=None):
	#affichage du date
	date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	day_month=datetime.now().strftime('%d-%m')
	hours=datetime.now().strftime('%H:%M:%S')
	#calcul des jours restants pour chaque employé suivant une condition

	if (day_month == '01-01'):
		#affichage des emplyées
		employees=self.pool.get('hr.employee').search(cr,uid,[],context=context)
		#pour chaque employé, on affiche le nbre de jours de congé et les jours restants
		for emp in range(len(employees)):
			emp_id=employees[emp]
			cr.execute('SELECT jr_cong_ann FROM hr_employee WHERE id=%s',(emp_id,))
			lines = cr.dictfetchall()
			for line in lines :
				jr_cong_ann=line['jr_cong_ann']
				cr.execute("INSERT INTO hr_holidays (number_of_days,state,employee_id,holiday_status_id,type,holiday_type) VALUES ('%s','%s','%s','%s','%s','%s')" %(jr_cong_ann, 'validate', emp_id, '1', 'add', 'employee'))

