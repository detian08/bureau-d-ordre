# encoding: utf-8
import JasperDataParser
from openerp.jasper_reports import jasper_report
from openerp import pooler
import time
import datetime
from operator import itemgetter

# import base64
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
###########################################################################################

	def generate_records(self, cr, uid, ids, data, context):
		print 'data.............',data

		pool = pooler.get_pool(cr.dbname)
		result = []
		if 'form' in data:
			dateAuj = time.strftime('%d-%m-%Y')
			for secteur in data['form']['sect_act_ids']:
				print secteur

			#oe_sect_act_ids = data['form']['oe_sect_act_ids'][0]
			#sect_act_name = data['form']['oe_sect_act_ids'][1]

				cr.execute('SELECT partner_id FROM res_partner_res_partner_category_rel WHERE category_id =' + str(secteur))
				res = cr.fetchall()
				op_eco_ids = [x[0] for x in res]
				print 'Liste des opérateurs économiques :',op_eco_ids

				if op_eco_ids:
					for op in op_eco_ids:
						print '',op
						partner_name=self.pool.get('res.partner').browse(cr,uid,op).name
						print 'partner',partner_name
						data = {
							'partner_name': partner_name,
                       				        'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",

						}
						result.append(data)
					print 'data..............',data
		print 'resultat: ',result
		return result


########################################################################################################

	
		
jasper_report.report_jasper('report.jasper_oe_secteurs_activite_print', 'res.partner', parser=jasper_client, )
