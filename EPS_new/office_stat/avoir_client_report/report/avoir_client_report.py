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
from datetime import datetime
import base64
import os
#import netsvc
from openerp.osv import fields, osv
from openerp.tools.translate import _

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
        print"********************000"

        pool= pooler.get_pool(cr.dbname)
        result=[]
        if 'form' in data:
            #from_date = data['form']['date_aujourd']
            dateAuj = time.strftime('%d-%m-%Y %H:%M')
            total_amount_total=0
            total_amount_untaxed=0

            reg_ids = pool.get('account.invoice').search(cr, uid, [('type', '=', 'out_refund'), ('state', '!=', 'paid')])
            print"********************111"
            
           
            reg_objs = pool.get('account.invoice').browse(cr, uid, reg_ids)
            print"********************222", reg_objs

            if reg_objs:
                print"********************333"

                for reg in reg_objs:

                    total_amount_total = total_amount_total+reg.amount_total
                    total_amount_untaxed = total_amount_untaxed + reg.amount_untaxed

                    print"...................total****.", total_amount_total

                    data={
                        'partner_id': reg.partner_id["name"],
                        'date_invoice':reg.date_invoice,
                        'amount_untaxed':reg.amount_untaxed,
                        'amount_total': reg.amount_total,
                        'number': reg.number,
                        'etat': reg.state,
                        'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                        'total_amount_total': total_amount_total,
                        'total_amount_untaxed': total_amount_untaxed,
                        'dateAuj':dateAuj,

                    }
                    print"...................data****.", data

                    result.append(data)

            else :
                   data={
                            'partner_id':'',
                            'date_invoice':'',
                            'amount_untaxed':'',
                            'amount_total':'',
                            'total_amount_untaxed': total_amount_untaxed,
                            'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                            'total_amount_total': total_amount_total,
                            'number': '',
                            'etat':'',
                           'dateAuj':dateAuj,

                        }
                   result.append(data)
        return result

jasper_report.report_jasper('report.jasper_avoir_client_print', 'account.invoice', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
