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

            #date_fin  = data['form']['date_fin']
            #date_debut = data['form']['date_debut']
            dateAuj = time.strftime('%d-%m-%Y %H:%M')
            total = 0
            caution_ids = self.pool.get('office.caution').search(cr, uid, [('libere','=',False)])
            
            caution_objs = self.pool.get('office.caution').browse(cr, uid, caution_ids)




            if caution_objs:
                for caut in caution_objs:
                    total = total + caut.montant
                    print"...................total****.", total
                    
                    data={
                        'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                        'montant':caut.montant,
                        'partenaire':caut.partner_id.name,
                        'description':caut.description,
                        'total': total,
                        'type':caut.tt,
                        'date':caut.date_caution,
                        'dateAuj': dateAuj,
                    }
                    result.append(data)
            else :
                data={
                        'montant':'',
                        'partenaire':'',
                        'description':'',
                        'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                        'total': total,
                        'type':'',
                        'date':'',
                        'dateAuj': dateAuj,

                }
                result.append(data)
                  
        return result

jasper_report.report_jasper('report.jasper_etat_caution_print', 'office.caution', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
