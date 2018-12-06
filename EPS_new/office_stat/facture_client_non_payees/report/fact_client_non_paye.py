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
            total=0
            total_amount_total=0
            total_amount_total_reg=0
            total_amount_total_reg2=0
            total_amount_total_inv2=0
            total_amount_untaxed_reg=0
            total_amount_untaxed_reg2=0
            total_amount_untaxed=0
            total_amount_untaxed_inv2=0
            total_reste_a_payer_reg=0
            total_reste_a_payer_inv2=0
            dateAuj = time.strftime('%d-%m-%Y %H:%M')

            #Facture
            reg_ids = self.pool.get('account.invoice').search(cr, uid, [('state','!=','paid'), ('state', '!=', 'cancel'),('type','=','out_invoice')])
            reg_objs = pool.get('account.invoice').browse(cr, uid, reg_ids)
            
            inv_pick_ids = self.pool.get('invoice.picking').search(cr, uid, [('state','=','draft'),('type','=','out_invoice')])
            inv_pick_objs = pool.get('invoice.picking').browse(cr, uid, inv_pick_ids)

            for reg in reg_objs:
                type_reg = reg.type
                print"========type", type_reg

            for reg1 in reg_objs:
                total_amount_total_reg = total_amount_total_reg + reg1.amount_total
                print"=======total_amount_total_reg", total_amount_total_reg
                total_amount_untaxed_reg = total_amount_untaxed_reg + reg1.amount_untaxed
                print"=======total_amount_untaxed_reg", total_amount_untaxed_reg
                total_reste_a_payer_reg = total_reste_a_payer_reg + reg1.reste_a_payer
                print"=======total_reste_a_payer_reg", total_reste_a_payer_reg

            for reg2 in inv_pick_objs:
                total_amount_total_reg2 = total_amount_total_reg2 + reg2.amount_total
                print"=======total_amount_total_reg2", total_amount_total_reg2
                total_amount_untaxed_reg2 = total_amount_untaxed_reg2 + reg2.amount_untaxed
                print"=======total_amount_untaxed_reg2", total_amount_untaxed_reg2


            #Avoir

            reg_av_ids = self.pool.get('account.invoice').search(cr, uid,
                                                                 [('state', '!=', 'paid'), ('state', '!=', 'cancel'),
                                                                  ('type', '=', 'out_refund')])
            reg_av_objs = pool.get('account.invoice').browse(cr, uid, reg_av_ids)

            inv_av_pick_ids = self.pool.get('invoice.picking').search(cr, uid, [('state', '=', 'draft'),
                                                                                ('type', '=', 'out_refund')])
            inv_av_pick_objs = pool.get('invoice.picking').browse(cr, uid, inv_av_pick_ids)

            for inv in reg_av_objs:
                type_inv = inv.type
                print"========type", type_inv

            for inv in inv_av_pick_objs:
                total_amount_total = total_amount_total + inv.amount_total
                print"=======total", total_amount_total
                total_amount_untaxed = total_amount_untaxed + inv.amount_untaxed
                print"=======total_amount_untaxed", total_amount_untaxed


            for inv2 in reg_av_objs:
                total_amount_total_inv2 = total_amount_total_inv2 + inv2.amount_total
                print"=======total_inv2", total_amount_total_inv2
                total_amount_untaxed_inv2 = total_amount_untaxed_inv2 + inv2.amount_untaxed
                print"=======total_inv2", total_amount_untaxed_inv2
                total_reste_a_payer_inv2 = total_reste_a_payer_inv2 + inv2.reste_a_payer
                print"=======total_reste_a_payer_inv2", total_reste_a_payer_inv2

            total_amount_total = total_amount_total_reg+ total_amount_total_reg2- total_amount_total- total_amount_total_inv2
            print"*****total******", total_amount_total

            total_amount_untaxed_total = total_amount_untaxed_reg + total_amount_untaxed_reg2 - total_amount_untaxed - total_amount_untaxed_inv2
            print"*****total_amount_untaxed_total******", total_amount_untaxed_total

            total_reste_a_payer_total = total_reste_a_payer_reg  - total_reste_a_payer_inv2
            print"*****total_reste_a_payer_total******", total_reste_a_payer_total

            #Facture
            if reg_objs:
                for reg in reg_objs:
                        total=total+reg.reste_a_payer
                       
                        data={
                            'num_fac':reg.number,
                            'client':reg.partner_id["name"],
                            'date':reg.date_invoice,
                            'montant':reg.amount_total,
                            'reste_a_payer':reg.reste_a_payer,
                            'etat':dict(self.pool.get('account.invoice').fields_get(cr, uid, allfields=['state'], context=context)['state']['selection'])[reg.state],#reg.state.name,
                            'MHTVA':reg.amount_untaxed,
                            # 'total':total,
                            'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                            'dateAuj':dateAuj,
                            'type': 'Facture',
                            'total_amount_total': total_amount_total,
                            'total_amount_untaxed_total': total_amount_untaxed_total,
                            'total_reste_a_payer_total': total_reste_a_payer_total
                            
                        } 
                        result.append(data)
            if inv_pick_objs:
                for inv_pick in inv_pick_objs:
                    total=total+inv_pick.amount_total
                    data={
                            'num_fac':inv_pick.internal_number,
                            'client':inv_pick.partner_id["name"],
                            'date':inv_pick.date_invoice_picking,
                            'montant':inv_pick.amount_total,
                            # 'reste_a_payer':inv_pick.amount_total,
                            'etat':dict(self.pool.get('invoice.picking').fields_get(cr, uid, allfields=['state'], context=context)['state']['selection'])[inv_pick.state],#reg.state.name,
                            'MHTVA':inv_pick.amount_untaxed,
                            # 'total':total,
                            'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                            'dateAuj':dateAuj,
                            'type': 'Facture',
                            'total_amount_total': total_amount_total,
                            'total_amount_untaxed_total': total_amount_untaxed_total,
                            'total_reste_a_payer_total': total_reste_a_payer_total
                            
                    } 
                    result.append(data)
  ###################################################################################"
            # Avoir

            if reg_av_objs:
                for reg in reg_av_objs:
                    total = total + reg.reste_a_payer

                    data = {
                        'num_fac': reg.number,
                        'client': reg.partner_id["name"],
                        'date': reg.date_invoice,
                        'montant': str('-') + str(reg.amount_total),
                        'reste_a_payer': str('-') + str(reg.reste_a_payer),
                        'etat': dict(
                            self.pool.get('account.invoice').fields_get(cr, uid, allfields=['state'],
                                                                        context=context)[
                                'state']['selection'])[reg.state],  # reg.state.name,
                        'MHTVA': str('-') + str(reg.amount_untaxed),
                        # 'total': total,
                        'stat_path': os.getcwd() + "/openerp/addons/office_stat/",
                        'dateAuj': dateAuj,
                        'total_amount_total': total_amount_total,
                        'total_amount_untaxed_total': total_amount_untaxed_total,
                        'total_reste_a_payer_total': total_reste_a_payer_total,
                        'type': 'Avoir'

                    }
                    result.append(data)
            if inv_av_pick_objs:
                for inv_pick in inv_av_pick_objs:
                    total = total + inv_pick.amount_total
                    data = {
                        'num_fac': inv_pick.internal_number,
                        'client': inv_pick.partner_id["name"],
                        'date': inv_pick.date_invoice_picking,
                        'montant': str('-') + str(inv_pick.amount_total),
                        # 'reste_a_payer': str('-') + str(inv_pick.amount_total),
                        'etat': dict(
                            self.pool.get('invoice.picking').fields_get(cr, uid, allfields=['state'], context=context)[
                                'state']['selection'])[inv_pick.state],  # reg.state.name,
                        'MHTVA': str('-') + str(inv_pick.amount_untaxed),
                        # 'total': total,
                        'stat_path': os.getcwd() + "/openerp/addons/office_stat/",
                        'dateAuj': dateAuj,
                        'total_amount_total': total_amount_total,
                        'total_amount_untaxed_total': total_amount_untaxed_total,
                        'total_reste_a_payer_total': total_reste_a_payer_total,
                        'type': 'Avoir'

                    }
                    result.append(data)



            if not reg_objs and not inv_pick_objs and not reg_av_objs and not inv_av_pick_objs:
                data = {
                    'num_fac': '',
                    'client': '',
                    'date': '',
                    'montant': '',
                    'reste_a_payer': '',
                    'etat': '',
                    'MHTVA': '',
                    # 'total': 0,
                    'stat_path': os.getcwd() + "/openerp/addons/office_stat/",
                    'dateAuj': dateAuj,
                    'type': '',
                    'total_amount_total': '',
                    'total_amount_untaxed_total':'',
                    'total_reste_a_payer_total':''

                }

                result.append(data)
                        
        return result

jasper_report.report_jasper('report.jasper_fact_client_non_paye_print', 'account.invoice', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
