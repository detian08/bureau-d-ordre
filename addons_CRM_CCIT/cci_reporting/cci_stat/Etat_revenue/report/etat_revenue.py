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
        uid = 1
        pool = pooler.get_pool(cr.dbname)
        result = []
        if 'form' in data:
            # from_date = data['form']['date_aujourd']
            dateAuj = time.strftime('%d-%m-%Y')
            total_realise = 0
            total_fail = 0
            product_ids = data['form']['product_ids']
            print '****product_id..........', product_ids
            # date_debut = data['form']['date']
            # print '****date_debut', date_debut
            # year = date_debut[0:4]
            # print"*******year******",year
            #date_acc = data['form']['year']
            #print"*******date_acc******", date_acc ,('annee','=',date_acc)


            for product_id in product_ids :
                print '......................',product_id
                #cash_ids = pool.get('product.template').search(cr, uid, [('name', '=', product_id)])
                cash_objs = pool.get('product.template').browse(cr, uid, product_id)
                # -------------------------------- Revenu Réalisée --------------------------------------------------
                reg_ids = pool.get('crm.lead').search(cr, uid, [('product_id', '=', cash_objs.id),('stage_id','=',6)])

                reg_objs = pool.get('crm.lead').browse(cr, uid, reg_ids)

                if reg_objs:
                    for reg in reg_objs:
                        total_realise = (round(total_realise,2) + round(reg.planned_revenue,2))
                        if reg.planned_revenue == 0:
                            won_revenue = 0.00
                        else:
                            won_revenue = reg.planned_revenue
                    data = {
                        'name': reg.name,
                        # 'date': date_debut,
                        #'year': date_acc,
                       # 'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",
                         #'stat_path' :os.getcwd()+"/openerp/jasper_reports/images/",
                        'planned_revenue': won_revenue,
                        'product_id': reg.product_id["name"],
                        # 'total_realise': total_realise,
                        'dateAuj': dateAuj,
                        'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",

                    }

                    result.append(data)


#-------------------------------- Revenu Perdu --------------------------------------------------

                fail_ids = pool.get('crm.lead').search(cr, uid,[('product_id', '=', cash_objs.id), ('stage_id', '=', 7)])

                fail_objs = pool.get('crm.lead').browse(cr, uid, fail_ids)

                if fail_objs:
                    for fail in fail_objs:
                        total_fail = total_fail + fail.planned_revenue
                        if fail.planned_revenue == 0:
                            fail_revenue = 0.00
                        else:
                            fail_revenue = fail.planned_revenue
                    data = {
                        'name': fail.name,
                        'fail_revenue': fail_revenue,
                        'product_id': fail.product_id["name"],
                        'total_fail': total_fail,
                        'total_realise': total_realise,
                        'dateAuj': dateAuj,
                        'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",

                    }
                    print"...................data_fail****.", data

                    result.append(data)
                else:
                        data = {
                            'name': '',
                            'product_id': '',
                            'product_id': '',
                            'fail_revenue': 0.00,
                            'date': '',
                            'total': 0.00,
                            'total_fail': total_fail,
                            'total_realise': total_realise,
                            'dateAuj': dateAuj,
                            'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",

                        }
                        result.append(data)
        return result


jasper_report.report_jasper('report.jasper_revenue_print', 'crm.lead', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
