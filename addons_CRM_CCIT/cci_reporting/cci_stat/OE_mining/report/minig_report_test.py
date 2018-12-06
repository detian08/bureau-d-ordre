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






    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        res = []
        if context.get('special_display_name', special_display_name):
            print 'special_display_name.....',special_display_name
        if special_display_name == 'cci.next.wizard.survey':
            for record in self.browse(cr, uid, ids, context=context):
                print 'record.....',record
                question_id = record.question_id
                print 'question_id.....',question_id
                reponse_id = record.reponse_id
                print 'reponse_id.....',reponse_id
                res.append(record.question_id, record.reponse_id)
                   # else:
                        # Do a for and set here the standard display name, for example if the standard display name were name, you should do the next for
                        #for record in self.browse(cr, uid, ids, context=context):
                          #  res.append(record.id, record.name)
        return res
        print 'res.....',res































        if 'form' in data:
	
            survey_ids = data['form']['survey_ids']

            consultation_ids = data['form']['consultation_ids']


            product_id = data['form']['product_id'][0]

            product_name = data['form']['product_id'][1]

            tags = data['form']['tags_id']

            dateAuj = time.strftime('%d-%m-%Y')
            data={
			    'dateAuj': dateAuj,
                'product_name':product_name,
               	'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",
            }

            result.append(data) 
            if survey_ids:
                for survey_id in survey_ids:
                    survey_user_input = self.pool.get('survey.user_input').search(cr, uid, [('survey_id','=',survey_id)])
                    #cr.execute('SELECT partner_id FROM survey_user_input WHERE survey_id=%s',(survey_id,))
                    #res = cr.dictfetchall()

                    for user_input in survey_user_input:

                        partner_name=self.pool.get('survey.user_input').browse(cr,uid,user_input).partner_id.name

                        data={
                            'partner_name':partner_name,

                        }

                    result.append(data) 


        return result

jasper_report.report_jasper('report.jasper_oe_minig_print', 'res.partner', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
