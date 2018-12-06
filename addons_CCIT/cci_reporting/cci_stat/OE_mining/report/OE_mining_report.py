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
from datetime import date
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
			#product_obj = self.pool.get('rproduct.template')
			#op_eco_obj = product_obj.browse(cr, uid, product_id)

            survey_ids = data['form']['survey_ids']
            print '****survey_ids', survey_ids
            consultation_ids = data['form']['consultation_ids']
            print '****consultation_ids', consultation_ids

            product_id = data['form']['product_id'][0]
            print '****product_id', product_id
            product_name = data['form']['product_id'][1]
            print '****product_name', product_name
            tags = data['form']['tags_id']
            print '****tags_id', tags
            dateAuj = time.strftime('%d-%m-%Y')
            data={
			    'dateAuj': dateAuj,
                'product_name':product_name,
               	'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",
            }

            result.append(data) 
            if survey_ids:
                for survey_id in survey_ids:
                    print 'survey_id.....',survey_id
                    survey_user_input = self.pool.get('survey.user_input').search(cr, uid, [('survey_id','=',survey_id)])
                    #cr.execute('SELECT partner_id FROM survey_user_input WHERE survey_id=%s',(survey_id,))
                    #res = cr.dictfetchall()

                    for user_input in survey_user_input:
                        print 'res :',user_input
                        partner_name=self.pool.get('survey.user_input').browse(cr,uid,user_input).partner_id.name
                        print 'partner',partner_name




                        data={
                            'partner_name':partner_name,

                        }

                    result.append(data) 
######################################################afficher les opérateurs économiques pour les consultations############

            
            if consultation_ids:
                for consult_id in consultation_ids:
                    print 'consult_id.....',consult_id
                    #today = date.today()
                    #annee = today.year
                    exist=self.pool.get('cci.consultation').browse(cr,uid,consult_id).op_eco_exist
                    print 'exist: ',exist
                    if exist:#true
                        partner_name=self.pool.get('cci.consultation').browse(cr,uid,consult_id).op_eco_id.name
                        print 'partner',partner_name

                    else:
                        partner_name=self.pool.get('cci.consultation').browse(cr,uid,consult_id).op_eco_new
                        print 'partner',partner_name
                    data={

                        'partner_name':partner_name,

                    }
                    result.append(data) 

####################################################consultation_tags###################

            if tags:
                print 'tags',tags
                list_tags = tags.split(",")


                #for tag in list_tags:
                 #       print 'tag',tag

                tag_ids = self.pool.get('cci.consultation.tags').search(cr, uid, [('name','in',list_tags)])
                print 'tag_ids',tag_ids
                for tag_id in tag_ids:
                    consultations_ids=self.pool.get('cci.consultation').search(cr,uid,[('consult_tag','=',tag_id)])
                    print 'consultations_ids:',consultations_ids
                    exist=self.pool.get('cci.consultation').browse(cr,uid,consultations_ids).op_eco_exist
                    print 'exist: ',exist
                    if exist:#true
                        partner_name=self.pool.get('cci.consultation').browse(cr,uid,consultations_ids).op_eco_id.name
                        print 'partner',partner_name

                    else:
                        partner_name=self.pool.get('cci.consultation').browse(cr,uid,consultations_ids).op_eco_new
                        print 'partner',partner_name

                    data={

                        'partner_name':partner_name,
                    }
                    result.append(data)
        print 'res: ',result
        return result

jasper_report.report_jasper('report.jasper_oe_minig_print', 'res.partner', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
