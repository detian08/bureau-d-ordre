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
            dateAuj = time.strftime('%d-%m-%Y %H:%M')
            total=0

            reg_ids = self.pool.get('reglement.piece').search(cr, uid, [('mode_reglement','=','Chèque'),('type','=','in'),('state','in',['integrated'])])
            
            reg_objs = pool.get('reglement.piece').browse(cr, uid, reg_ids)
            print"+++++++++++++++reg_objs", reg_objs
            if reg_objs:
                for reg in reg_objs:
                        total=total+reg.montant_piece
                        print "++++++++++++++total", total
                        print "++++++++++++++reg.num_cheque_traite", reg.num_cheque_traite
                        print "++++++++++++++reg.partner_id", reg.partner_id["name"]

                        print "++++++++++++++reg.date_encaissement", reg.date_encaissement

                        print "++++++++++++++dateAuj", dateAuj

                        data={
                            'num_cheq':reg.num_cheque_traite,
                            'Designation':reg.partner_id["name"],
                            'date':reg.date_encaissement,
                            'montant':reg.montant_monnaie_local,
                            'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                            'total':total,
                            'dateAuj':dateAuj,
                            
                        }
                        print"...................data****.", data

                        result.append(data)
                print"..................****.data****.", result.append(data)

            else :
                data={
                            'num_cheq':'',
                            'Designation':'',
                            'date':'',
                            'montant':'',
                            'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                            'total':total,
                            'dateAuj':dateAuj,
                            
                        } 
                result.append(data)
                        
        return result

jasper_report.report_jasper('report.jasper_cheques_circulation_print', 'reglement.piece', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
