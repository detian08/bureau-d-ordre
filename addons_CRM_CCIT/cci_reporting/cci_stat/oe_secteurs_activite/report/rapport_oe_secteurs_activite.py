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
		result = []
		if 'form' in data:

			sect_act_ids = data['form']['sect_act_ids']
			dateAuj = time.strftime('%d-%m-%Y')

			data = {
				'dateAuj': dateAuj,
				'stat_path': os.getcwd() + "/openerp/addons/cci_stat/",
			}
			result.append(data)
			for secteur in sect_act_ids:
				sect_act_name=self.pool.get('res.partner.category').browse(cr,uid,secteur,context).name

				cr.execute('SELECT partner_id FROM res_partner_res_partner_category_rel WHERE category_id =' + str(secteur))
				res = cr.fetchall()
				op_eco_ids = [x[0] for x in res]

				if op_eco_ids:
					for op in op_eco_ids:
						partner_name=self.pool.get('res.partner').browse(cr,uid,op).name
						data = {
							'sect_act_name':sect_act_name,
							'partner_name': partner_name,
						}
						result.append(data)
				# else:
				# 	data = {
				# 		'sect_act_name': '',
				# 		'partner_name': '',
				# 	}
				# 	result.append(data)

		print 'resultat: ',result
		return result


########################################################################################################

	
		
jasper_report.report_jasper('report.jasper_oe_secteurs_activite_print', 'res.partner', parser=jasper_client, )
