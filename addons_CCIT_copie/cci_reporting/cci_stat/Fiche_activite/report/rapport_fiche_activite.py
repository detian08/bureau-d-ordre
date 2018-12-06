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
		total_mont_adh = 0
		total_mont_op = 0
		list_category = []
		list_product = []
		list_categ_name = []
		pool = pooler.get_pool(cr.dbname)
		result = []
		if 'form' in data:

			print 'data.............',data
			dateAuj = time.strftime('%d-%m-%Y %H:%M')
			responsable_id = data['form']['responsable_id'][0]
			responsable_name = data['form']['responsable_id'][1]
			date_debut = data['form']['date_debut']
			date_fin = data['form']['date_fin']
			print '',responsable_id


			#date_debut = datetime.datetime.strptime(date_debut, "%Y-%m-%d").strftime('%d-%m-%Y')
			#date_fin = datetime.datetime.strptime(date_fin, "%Y-%m-%d").strftime('%d-%m-%Y')
			dateAuj = time.strftime('%d-%m-%Y %H:%M')
			print '',date_debut,'',date_fin
			#######autre activité
         
			event_ids = pool.get('crm.lead.activity').search(cr, uid, [('create_uid', '=', responsable_id),('date_action', '>=', date_debut),('date_action', '<=', date_fin)])
			print 'event_ids :',event_ids
			event_objs = pool.get('crm.lead.activity').browse(cr, uid, event_ids)

			if event_ids:
				for event in event_objs:
					print 'event.....',event
					event_type = pool.get('crm.lead.activity').browse(cr, uid, event.id).type
					event_name = pool.get('crm.lead.activity').browse(cr, uid, event.id).name
					event_date = pool.get('crm.lead.activity').browse(cr, uid, event.id).create_date
					print 'event_type',event_type,'event_name...',event_name
					data = {
						#'date_op': datetime.datetime.strptime(op.date_debut,"%Y-%m-%d"),
						#'date_debut': datetime.datetime.strptime(op.date_debut,"%Y-%m-%d"),
						'dateAuj': dateAuj,
						'date_debut': date_debut,
						'date_fin': date_fin,
						'event_name':event_name,
						'type':event_type,
						'create_date':event_date,
                        			'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",

					}
					result.append(data)
				print 'data..............',data

         		#######consultation
			print 'cons ....',pool.get('cci.consultation') 
			consult_ids = pool.get('cci.consultation').search(cr, uid, [('type_id', '=', responsable_id),('date_cons', '>=', date_debut),('date_cons', '<=', date_fin)])
			print 'consult_ids.....',consult_ids
			consult_objs = pool.get('cci.consultation').browse(cr, uid, consult_ids)
			print 'consult_ids :',consult_ids
			if consult_ids:

				for consultation in consult_objs:

					data = {
						#'date_op': datetime.datetime.strptime(op.date_debut,"%Y-%m-%d"),
						#'date_debut': datetime.datetime.strptime(op.date_debut,"%Y-%m-%d"),
						'dateAuj': dateAuj,
						'date_debut': date_debut,
						'date_fin': date_fin,
						'responsable_name':responsable_name,
						'nom_op': u'À planifier une consultation',
                       				'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",

					}
					result.append(data)
				print 'data..............',data
		#####opérateur économique

					#partner_id=self.pool.get('res.partner').browse(cr,uid,op).id
					#print 'partner',partner_id
					#data = {
						#'partner_id': partner_id,
						#'nom_op': u'À avoir une consultation',
					#}
					#result.append(data)
				#print 'data..............',data


		return result





########################################################################################################

	
		
jasper_report.report_jasper('report.jasper_fiche_activite_print', 'res.partner', parser=jasper_client, )
