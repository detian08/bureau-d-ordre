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
	    print "data..............",data
	    product_id = data['form']['product_id'][0] ##get id
	    product_name = data['form']['product_id'][1]##get name
	    #question_id = data['form']['question_id'][0]
	    #question = data['form']['question_id'][1]
            #value_text = data['form']['value_text'][0]
            #value_text = data['form']['value_text'] ### get les questions ##pour get sondage
            #print '****value_text', value_text
            # page_ids = data['form']['page_ids'][1]
            # print '****page_ids', page_ids
            dateAuj = time.strftime('%d-%m-%Y %H:%M')
            total=0
	    #cr.execute('SELECT partner_id FROM survey_user_input ,survey_question q,survey_label ,survey_user_input_line WHERE 			survey_user_input.product_id=%s and survey_label.question_id=%s and survey_user_input_line.value_suggested =%s Group BY partner_id',(product_id,consultation_ids))
	    product_obj = cr.dictfetchall()
	    print 'product.....',product_obj

            #sond_ids = pool.get('survey.survey').search(cr, uid, [('title', '=', value_text)])
            #sond_objs = self.pool.get('survey.user_input').browse(cr, uid, sond_ids)
            if product_obj:
                for product in product_obj:

                    data={
                        'name':survey_name,
                        'product':product_name,
			#'operateur':survey_title,
			#'question':question,
                        #'product_id':sond.product_id['name'],
                    }

                result.append(data)
		print 'result .....',result

                              
        #return result

jasper_report.report_jasper('report.jasper_oe_mining_print', 'product.template', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c


















