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

	def generate_records(self, cr, uid, ids, data, context):
		total_mont_adh = 0
		total_mont_op = 0
		list_category = []
		list_product = []
		list_categ_name = []
		pool = pooler.get_pool(cr.dbname)
		result = []
		if 'form' in data:
			partner_obj = self.pool.get('res.partner')
			dateAuj = time.strftime('%d-%m-%Y')
			op_eco_id = data['form']['op_eco_id'][0]

			op_eco_obj = partner_obj.browse(cr, uid, op_eco_id)
			street = partner_obj.browse(cr, uid, op_eco_id).street
			street2 = partner_obj.browse(cr, uid, op_eco_id).street2
			city = partner_obj.browse(cr, uid, op_eco_id).city
			zip = partner_obj.browse(cr, uid, op_eco_id).zip
			country_id = partner_obj.browse(cr, uid, op_eco_id).country_id.id
			country= self.pool.get('res.country').browse(cr, uid, country_id).name

			ops_ids = pool.get('crm.lead').search(cr, uid, [('partner_id', '=', op_eco_id),('stage_id.name','=','Won')])
			ops_objs = pool.get('crm.lead').browse(cr, uid, ops_ids)
			
			currency_id = pool.get('res.company').browse(cr, uid, 1).currency_id.id
			print '',currency_id
			currency = pool.get('res.currency').browse(cr, uid, currency_id).symbol
			print 'symbol...',currency

			if ops_objs:
				for op in ops_objs:
					total_mont_op = total_mont_op + op.planned_revenue
					data = {
						'date_op': datetime.datetime.strptime(op.date_debut,"%Y-%m-%d"),
						'dateAuj': dateAuj,
						'currency':currency,
						'nom_op_eco':op_eco_obj[0].name,
						'street':street,
						'street2':street2,
						'city':city,
						'zip':zip,
						'country':country,
						'nom_op': u'Participer à ' + op.name,
						'mont_op': repr(op.planned_revenue),
						'mont_op_lost':'',
                                                'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",
					}
					result.append(data)

	
			cr.execute("SELECT category_id FROM res_partner_res_partner_category_rel WHERE partner_id =%s",(op_eco_id,))	
			lines = cr.dictfetchall()
			if lines :
				for line in lines:
					category_id = line['category_id']
					list_category.append(category_id)
				print 'list_category.....',list_category

				
				cr.execute('SELECT product_template_id FROM product_template_res_partner_category_rel WHERE res_partner_category_id in %s',(tuple(list_category),))
				lines_p = cr.dictfetchall()
				print 'lines_p..',lines_p
				for product in lines_p:
					product_template_id = product['product_template_id']


					categ_id = self.pool.get('product.template').browse(cr, uid, product_template_id, context=context).categ_id.id
					list_product.append(categ_id)

				cr.execute('SELECT crm_case_section_id FROM crm_case_section_product_category_rel WHERE product_category_id in %s',(tuple(list_product),))
				dict_section = cr.dictfetchall()
				print 'dict_section .....',dict_section
				if dict_section:
					print '...........yes'
					section_id=dict_section['crm_case_section_id']
					print 'section_id..',section_id

					section_code = self.pool.get('crm.case.section').browse(cr,uid,section_id,context=context).code
					section = self.pool.get('crm.case.section').browse(cr,uid,section_id,context=context).name
					data = {						
						'section':section,
						'section_code':section_code,
		                                'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",

					}
					result.append(data)

				for cat in list_category :
					category = self.pool.get('res.partner.category').browse(cr,uid,cat,context=context).name
					list_categ_name.append(category) 

					data = {						
						'category':category,
					}
					result.append(data)

			else:
				data = {
					'date_op': datetime.datetime.strptime(op.date_debut,"%Y-%m-%d"),
					'dateAuj': dateAuj,
					'nom_op_eco':op_eco_obj[0].name,
					'currency':currency,
					'street':street,
					'street2':street2,
					'city':city,
					'zip':zip,
					'country':country,
					'nom_op': '',
					'mont_op': '',
					'mont_op_lost':'',
					'section':'',
					'section_code':'',
					'category':'',
                                        'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",
				}
				result.append(data)
	


		return result
					#adh_ids = pool.get('membership.membership_line').search(cr, uid, [('partner', '=', op_eco_id)])
					#adh_lines_objs = pool.get('membership.membership_line').browse(cr, uid, adh_ids)
					#if adh_lines_objs:
					#	for adh in adh_lines_objs:
					#		adh_obj = pool.get('product.product').browse(cr, uid, adh.membership_id.id)
							#adh_date = time.strptime(adh.write_date)
					#		total_mont_adh = total_mont_adh + adh.member_price
					#		data = {
					#			'date_op':datetime.datetime.strptime(adh.write_date,"%Y-%m-%d %H:%M:%S"),
					#			'nom_op' : u'Adhésion ' + adh_obj.name_template,
					#			'mont_op':repr(adh.member_price),
					#		}
					#		result.append(data)

			
				#-----------------Sort operations by date--------------------
				#print "...............res",result[0:]
				# is equivalent to a shallow copied list of all elements starting from the 0-indexed 1
				#rows_by_date_op = sorted(result[2:], key=itemgetter('date_op'))

				#for obj in rows_by_date_op:
				#	if 'date_op' in obj:
				#		obj['date_op'] = datetime.datetime.strftime(obj['date_op'], "%d-%m-%Y")


				#rows_by_date_op.insert(0,result[0])

		#return rows_by_date_op
		
jasper_report.report_jasper('report.jasper_fiche_op_eco_print', 'res.partner', parser=jasper_client, )
