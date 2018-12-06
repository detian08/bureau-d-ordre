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
            print 'data: ',data['form']
            model = data['context']
            print '..............................',model
            dateAuj = time.strftime('%d-%m-%Y')


            if model == 'cci.next.wizard.survey':
                survey_id = data['form']['survey_id'][0]
                question_id = data['form']['question_id'][0]
                reponse_id = data['form']['reponse_id'][0]
                reponse_text = data['form']['reponse_text']
                print survey_id,question_id,reponse_id,reponse_text
                data = {
                    'dateAuj': dateAuj,
                    'stat_path': os.getcwd() + "/openerp/addons/cci_stat/",
                }
                result.append(data)

                if survey_id:
                    survey_user_input = self.pool.get('survey.user_input').search(cr, uid, [('survey_id','=',survey_id)]) #liste des réponses
                    print survey_user_input
                    for user_input in survey_user_input: ##parcourir les réponse
                        # reponse_id = self.pool.get('survey.label').search(cr,uid,[('value','=',reponse),('question_id','=',question_id)])
                        # print reponse_id[0]
                        user_input_line_id = self.pool.get('survey.user_input_line').search(cr,uid,[('user_input_id','=',user_input),('survey_id','=',survey_id),('question_id','=',question_id),('value_suggested','=',reponse_id)]) ##get the best line
                        print user_input_line_id
                        user_input_id = self.pool.get('survey.user_input_line').browse(cr,uid,user_input_line_id).user_input_id.id
                        print user_input_id
                        partner_name = self.pool.get('survey.user_input').browse(cr,uid,user_input_id).partner_id.name
                        print partner_name
                        data={
                            'partner_name':partner_name,
                        }

                    result.append(data)
######################################################afficher les opérateurs économiques pour les consultations############
            if model == 'cci.next.wizard.consultation':
                print 'data: ', data
                tags_ids = data['form']['tags_ids']
                print 'tags_ids.....', tags_ids
                data = {
                    'dateAuj': dateAuj,
                    'stat_path': os.getcwd() + "/openerp/addons/cci_stat/",
                }
                result.append(data)
                if tags_ids:


                        cr.execute('SELECT consult_id FROM consult_tag_rel WHERE tag_id in %s',(tags_ids,))
                        res = cr.fetchall()
                        consult_ids = [x[0] for x in res]
                        print 'consult_id: ', consult_ids
                        for consult_id in consult_ids:



                            #today = date.today()
                            #annee = today.year
                            exist= self.pool.get('cci.consultation').browse(cr,uid,consult_id).op_eco_exist
                            print 'exist....',exist

                            if exist:#true
                                print 'exist....', exist
                                partner_name=self.pool.get('cci.consultation').browse(cr,uid,consult_id).op_eco_id.name
                                print 'partner_name....', partner_name


                            else:
                                print 'exist....', exist
                                partner_name=self.pool.get('cci.consultation').browse(cr,uid,consult_id).op_eco_new
                                print 'partner_name....', partner_name


                            data={

                                'partner_name':partner_name,

                            }
                            result.append(data)
        return result

####################################################consultation_tags###################

jasper_report.report_jasper('report.jasper_oe_minig_print', 'res.partner', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
