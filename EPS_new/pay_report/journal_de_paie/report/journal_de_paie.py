# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import JasperDataParser  
from openerp.jasper_reports import jasper_report
from openerp import pooler
import time

from datetime import datetime,timedelta
import calendar
#import time, datetime
import base64
import os
from openerp import netsvc



class jasper_client(JasperDataParser.JasperDataParser):
    def __init__(self, cr, uid, ids, data, context):
        super(jasper_client, self).__init__(cr, uid, ids, data, context)

    def generate_data_source(self, cr, uid, ids, data, context):
        return 'records'

    def generate_parameters(self, cr, uid, ids, data, context):
        return {}

    def generate_properties(self, cr, uid, ids, data, context):
        return {}

    def generate_records(self, cr, uid, ids, data, context):
        #logger = netsvc.Logger()
        pool= pooler.get_pool(cr.dbname)
        result=[]
        
        if 'form' in data:
            date_du_jour = time.strftime('%d-%m-%Y %H:%M').split(" ")[0] 
            date = date_du_jour.split("-")[0]+"/"+date_du_jour.split("-")[1]+"/"+date_du_jour.split("-")[2]
            heure = time.strftime('%d-%m-%Y %H:%M').split(" ")[1]

            year= int(data['form']['year'])
            #mois= datetime.now().month
            mois = 12
            print "month=======", mois
            employee_ids=pool.get('hr.employee').search(cr, uid, [('slip_ids','!=','')])
            employee_objs=pool.get('hr.employee').browse(cr, uid, employee_ids)

            if employee_objs:

                for employee in employee_objs:
                    ## Fiche de paie 
                    from_date1=datetime(year,mois,1)
                    print "from_date1mmmmmmmmmmmmmm",from_date1
                    to_date1=datetime(year,mois,calendar.monthrange(year,mois)[1])
                    print "to_date1mmmmmmmmmmmmmm",to_date1
                    
                    payslip_ids1 = pool.get('hr.payslip').search(cr, uid, [('date_from','=',from_date1),('date_to','=',to_date1),('employee_id','=',employee.id)])
                    payslip_objs1 = pool.get('hr.payslip').browse(cr, uid, payslip_ids1)


                    if payslip_objs1:
                        
                        salire_base = 0
                        cnss = 0
                        irpp = 0
                        net = 0

                        for pay1 in payslip_objs1:
                            hr_payslip_line_ids = self.pool.get('hr.payslip.line').search(cr, uid, [('slip_id', '=', pay1.id)])
                            hr_payslip_line_obj = self.pool.get('hr.payslip.line').browse(cr,uid,hr_payslip_line_ids)

                            for hr_payslip_line in hr_payslip_line_obj :
                                if hr_payslip_line.code=='CNSS' :
                		            cnss=hr_payslip_line.total
                                if hr_payslip_line.code=='IRPP' :
                		            irpp=hr_payslip_line.total
                                if hr_payslip_line.code=='NET' :
                		            net=hr_payslip_line.total


                        data={
                            'date':date,
                            'heure':heure,
                            'mat':employee.num_chezemployeur,
                            'nom' : employee.name,
                            'ret_cnss':round(cnss,3),
                            'ret_irpp': round(irpp,3),
                            'salaire_net':round(net,3),
                            'stat_path' :os.getcwd()+"/addons_Polygarde/pay_report/",
                        }                         
                        result.append(data)
           
        return result

jasper_report.report_jasper('report.jasper_report_journal_de_paie_print', 'hr.payslip', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
