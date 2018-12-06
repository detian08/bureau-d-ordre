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
import datetime
import base64
import os
# import netsvc
from openerp.osv import fields, osv
from openerp.tools.translate import _

from operator import itemgetter


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

        pool = pooler.get_pool(cr.dbname)
        result = []
        print 'heloooo fiche Fournisseur report.............'
        if 'form' in data:
            dateAuj = time.strftime('%d-%m-%Y %H:%M')
            partner_id = data['form']['partner_id']
            date1 = data['form']['date1']
            date2 = data['form']['date2']
            print 'partner id............', partner_id[1]
            total_amount_total = 0
            total_amount_total_avoir = 0
            total_amount_total_bl = 0
            amount_untaxed_total = 0
            amount_untaxed_total_avoir = 0
            amount_untaxed_total_bl = 0
            print "OOOOOOOOOOOOOOOOO....." 
##--------------------factures Client du client-----------------------------------------------------
            invoice_line_ids = self.pool.get('account.invoice').search(cr, uid,
                                                                       [('partner_id', '=', partner_id[0]),
                                                                        ('type', '=', 'in_invoice'),
                                                                        ('state', '!=', 'cancel'),
                                                                        ('date_invoice','>=', date1),
                                                                        ('date_invoice','<=', date2)])
                                                                        #,('state', '!=', 'paid')])
            print "AAAAAAA....."
            #---total des factures
            inv_objs = pool.get('account.invoice').browse(cr, uid, invoice_line_ids)
            for inv2 in inv_objs:
                total_amount_total = total_amount_total + inv2.amount_total
                amount_untaxed_total = amount_untaxed_total + inv2.amount_untaxed
# --------------------------------------------------------------------------------------------------


##--------------------factures avoir du client------------------------------------------------------
            avoir_line_ids = self.pool.get('account.invoice').search(cr, uid,
                                                                    [('partner_id', '=', partner_id[0]),
                                                                     ('type', '=', 'in_refund'),
                                                                     ('state', '!=', 'cancel'),
                                                                     ('date_invoice','>=', date1),
                                                                     ('date_invoice','<=', date2)])
                                                                     #,('state', '!=', 'paid')])
            print "BBBBBBBBBB....."                                                  
            #---total des avoirs
            avoir_objs = pool.get('account.invoice').browse(cr, uid, avoir_line_ids)
            for inv3 in avoir_objs:
                total_amount_total_avoir = total_amount_total_avoir + inv3.amount_total
                amount_untaxed_total_avoir = amount_untaxed_total_avoir + inv3.amount_untaxed

# --------------------------------------------------------------------------------------------------

##--------------------factures BL du client------------------------------------------------------
            invoice_picking_ids = self.pool.get('invoice.picking').search(cr, uid,
                                                                          [('partner_id', '=', partner_id[0]),
                                                                           ('state', '=', 'draft'),
                                                                           ('type', '=', 'in_invoice'),
                                                                           ('date_invoice_picking','>=', date1),
                                                                           ('date_invoice_picking','<=', date2)])
            print "CCCCCCCC....." 
            #---total des facture BL du client
            invoice_picking_objs = self.pool.get('invoice.picking').browse(cr, uid, invoice_picking_ids)

            for inv4 in invoice_picking_objs:
                total_amount_total_bl = total_amount_total_bl + inv4.amount_total
                amount_untaxed_total_bl = amount_untaxed_total_bl + inv4.amount_untaxed

# --------------------------------------------------------------------------------------------------

            total_result = total_amount_total + total_amount_total_bl - total_amount_total_avoir
            print"==========total_result", total_result
            total_untaxed_result = amount_untaxed_total + amount_untaxed_total_bl - amount_untaxed_total_avoir
            print"==========total_untaxed_result", total_untaxed_result

#-----------------------lignes des factures BL du client--------------------------------------------


            if invoice_picking_objs:
                state = ''
                for obj in invoice_picking_objs:
                    if obj.state == 'draft':
                        state = 'brouillon'
                    elif obj.state == 'open':
                        state = 'ouverte'
                    else:
                        state = obj.state

                    if obj.internal_number == False:
                        internal_number = " - "
                    else:
                        internal_number = obj.internal_number
                    data = {
                        'partner_id': partner_id[1],
                        'number': internal_number,
                        'date_invoice': datetime.datetime.strptime(obj.date_invoice_picking, "%Y-%m-%d"),
                        'type': 'Facture BR',
                        'amount_untaxed': obj.amount_untaxed,
                        'amount_total': obj.amount_total,
                        'stat_path': os.getcwd() + "/openerp/addons/office_stat/",
                        'total_result': total_result,
                        'total_untaxed_result': total_untaxed_result,
                        'dateAuj': str(dateAuj),
                        'etat': state,
                    }
                    result.append(data)
# --------------------------------------------------------------------------------------------------------


#-----------------------lignes des factures avoir client--------------------------------------------------

            if avoir_objs:
                for reg in avoir_objs:
                    if reg.state == 'draft':
                        state = 'brouillon'
                    elif reg.state == 'open':
                        state = 'ouverte'
                    else:
                        state = reg.state

                    if reg.number == False:
                        number = " - "
                    else :
                        number = reg.number
                    # Avoir
                    data = {
                        'partner_id': reg.partner_id["name"],
                        'date_invoice': datetime.datetime.strptime(reg.date_invoice, "%Y-%m-%d"),
                        'amount_total': str('-') + str(reg.amount_total),
                        'amount_untaxed': str('-') + str(reg.amount_untaxed),
                        'number': number,
                        'etat': state,
                        'stat_path': os.getcwd() + "/openerp/addons/office_stat/",
                        'total_result': total_result,
                        'total_untaxed_result': total_untaxed_result,
                        'dateAuj': str(dateAuj),
                        'type': 'Avoir',

                    }
                    result.append(data)
                    print"...................data****.", data

# --------------------------------------------------------------------------------------------------------

#-----------------------lignes des factures client--------------------------------------------------------
            if inv_objs:
                for inv1 in inv_objs:
                    #total_inv = total_amount_total + inv1.amount_total
                    if inv1.state == 'draft':
                        state = 'brouillon'
                    elif inv1.state == 'open':
                        state = 'ouverte'
                    else:
                        state = inv1.state

                    if inv1.number == False:
                        number = " - "
                    else :
                        number = inv1.number
                    # Facture
                    data = {
                        'partner_id': inv1.partner_id["name"],
                        'date_invoice': datetime.datetime.strptime(inv1.date_invoice, "%Y-%m-%d"),
                        'amount_total': inv1.amount_total,
                        'amount_untaxed': inv1.amount_untaxed,
                        'number': number,
                        'etat': state,
                        'stat_path': os.getcwd() + "/openerp/addons/office_stat/",
                        'total_result': total_result,
                        'total_untaxed_result': total_untaxed_result,
                        'dateAuj': str(dateAuj),
                        'type': 'Facture',
                    }
                    print"...................data****.", data
                    result.append(data)
# --------------------------------------------------------------------------------------------------------



        #print "result====",result
        rows_by_date = sorted(result, key=itemgetter('date_invoice'))

        for obj in rows_by_date:
            if 'date_invoice' in obj:
                obj['date_invoice'] = datetime.datetime.strftime(obj['date_invoice'], "%d-%m-%Y")
        print "data====",data
        if not (inv_objs or avoir_objs or invoice_picking_objs):
            print "not data............"
            data = {
                'partner_id': partner_id[1],
                'date_invoice': '',
                'amount_untaxed': '',
                'amount_total': '',
                'number': '',
                'etat': '',
                'stat_path': os.getcwd() + "/openerp/addons/office_stat/",
                'total_result': '0',
                'total_untaxed_result': '0',
                'dateAuj': dateAuj,
                'type': '',
            }
            rows_by_date.append(data)

        # print rows_by_date
        return rows_by_date

jasper_report.report_jasper('report.jasper_fiche_fournisseur_print', 'account.invoice', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
