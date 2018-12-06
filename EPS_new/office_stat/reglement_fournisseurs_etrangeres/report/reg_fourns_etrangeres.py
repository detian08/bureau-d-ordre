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
        pool= pooler.get_pool(cr.dbname)
        result=[]
        if 'form' in data:
            #from_date = data['form']['date_from']
            #to_date = data['form']['date_to']
            dateAuj = time.strftime('%d-%m-%Y %H:%M')
            total=0      
            reg_ids = self.pool.get('account.invoice').search(cr, uid, [('state','!=','paid'),('type','=','in_invoice'),('currency_id','!=',137)])
            
            reg_objs = pool.get('account.invoice').browse(cr, uid, reg_ids)
            
            inv_picking_ids = self.pool.get('invoice.picking').search(cr, uid, [('state','=','draft'),('type','=','in_invoice'),('currency_id','!=',137),('partner_id.name','!=','EPS')])
            inv_picking_objs = self.pool.get('invoice.picking').browse(cr, uid, inv_picking_ids)

            if reg_objs:
                for reg in reg_objs:
                        
                        
                        currency=reg.currency_id.id,
                        currency_obj = self.pool.get('res.currency').browse(cr,uid,currency,context=context)
                        rate = currency_obj.rate_silent
                        montant_local=reg.amount_total / rate
                        total=total+montant_local
                        data={
                            'num_fac':reg.number,
                            'fournisseur':reg.partner_id["name"],
                            'date':reg.date_invoice,
                            'montant':reg.amount_total,
                            'montant_local':montant_local,
                            'rate':rate,
                            # 'date_reg':'',
                            'date_echeance': reg.date_due,
                            'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                            'total':total,
                            'dateAuj':dateAuj,
                            
                        } 
                        result.append(data)
                    
            if inv_picking_objs:
                for inv_picking in inv_picking_objs  :
                    currency_obj = self.pool.get('res.currency').browse(cr,uid,inv_picking.currency_id.id,context=context)
                    rate = currency_obj.rate_silent
                    montant_local=inv_picking.amount_total / rate
                    total+=(inv_picking.amount_total/currency_obj.rate_silent)
                    data={
                            'num_fac':inv_picking.internal_number,
                            'fournisseur':inv_picking.partner_id["name"],
                            'date':inv_picking.date_invoice_picking,
                            'montant':inv_picking.amount_total,
                            'montant_local':montant_local,
                            'rate':rate,
                            # 'date_reg':'',
                            'date_echeance': reg.date_due,
                            'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                            'total':total,
                            'dateAuj':dateAuj,
                            
                    } 
                    result.append(data)                        
            if not inv_picking_objs and not reg_objs :
                data={
                            'num_fac':'',
                            'fournisseur':'',
                            'date':'',
                            'montant':'',
                            'montant_local':'',
                            'rate':'',
                            # 'date_reg':'',
                            'date_echeance': reg.date_due,
                            'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                            'total':total,
                            'dateAuj':dateAuj,
                            
                        } 
                result.append(data)
                
                        
        return result

jasper_report.report_jasper('report.jasper_reg_fourns_etrangeres_print', 'account.invoice', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c

###################"""""""""""""""""""
