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
# import netsvc
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

        pool = pooler.get_pool(cr.dbname)
        result = []
        uid = 1
        if 'form' in data:
            # from_date = data['form']['date_aujourd']
            dateAuj = time.strftime('%d-%m-%Y')
            product_id = data['form']['product_id'][1]
            cash_ids = pool.get('product.template').search(cr, uid, [('name', '=', product_id)])
            cash_objs = pool.get('product.template').browse(cr, uid, cash_ids)



            # prod_ids = pool.get('product.product').search(cr, uid, [('product_id', '=', product_id)])
            # print'..................prod_ids', prod_ids
            reg_ids = pool.get('crm.claim').search(cr, uid, [('product_id', '=', cash_objs.id)])
           
            reg_objs = pool.get('crm.claim').browse(cr, uid, reg_ids)

            if reg_objs:

                for reg in reg_objs:
                    if reg.state== "draft":
                        state = "Brouillon"
                    elif reg.state == "soumise":
                        state = "Soumise"
                    elif reg.state == "to_validate":
                        state = "En cours de traitement"
                    elif reg.state == "validate":
                        state = "Traité"
                    elif reg.state == "reject":
                        state = "Rejeté"
                    elif reg.state == "close":
                        state = "Cloturé"
                    print '......................',state
                    data = {
                        'objet': reg.name,
                        'partner': reg.partner_id["name"],
                        'date_reclamation': reg.date,
                        'echeance': reg.date_deadline,
                        'responsable': reg.user_id["name"],
                        'state':state,
                        'product_id': reg.product_id["name"],
                        'dateAuj': dateAuj,
                        'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",

                    }

                    result.append(data)

            else:
                data = {
                    'objet': '',
                    'partner':'',
                    'date_reclamation':'',
                    'echeance':'',
                    'responsable': '',
                    'product_id': '',
                    'dateAuj': dateAuj,
                    'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",

                }
                result.append(data)
        return result


jasper_report.report_jasper('report.jasper_claim_print', 'crm.claim', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
