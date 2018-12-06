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
		uid = 1
		total_mont_op = 0
		list_category = []
		list_product = []
		list_categ_name = []
		pool = pooler.get_pool(cr.dbname)
		result = []

		if 'form' in data:
			dateAuj = time.strftime('%Y-%m-%d')
			permanent = data['form']['permanent']
			date_debut = data['form']['date_debut']
			date_fin = data['form']['date_fin']
			state = data['form']['state']
			
			if permanent == True :
				ce_ids = pool.get('cci.courriel.entrant').search(cr, uid, [('date_courriel','=',dateAuj)])
				print ce_ids
				for ce in ce_ids:
					ref = self.pool.get('cci.courriel.entrant').browse(cr, uid, ce, context=context).ref_entrant
					date_courriel = self.pool.get('cci.courriel.entrant').browse(cr, uid, ce, context=context).date_courriel
					note_id = self.pool.get('cci.courriel.entrant').browse(cr, uid, ce, context=context).note_id
					type_id = self.pool.get('cci.courriel.entrant').browse(cr, uid, ce, context=context).type_id.name
					objet = self.pool.get('cci.courriel.entrant').browse(cr, uid, ce, context=context).objet
					name = self.pool.get('cci.courriel.entrant').browse(cr, uid, ce, context=context).name
					dept_id = self.pool.get('cci.courriel.entrant').browse(cr, uid, ce, context=context).dept_id.name
					data = {
						'ref': ref,
						'dateAuj': dateAuj,
						'date_courriel':date_courriel,
						'note_id':note_id,
						'type_id':type_id,
						'objet':objet,
						'name':name,
						'dept_id':dept_id,
					}
					result.append(data)
				print 'data..............',data
			if date_debut and date_fin and permanent != True:
				ce_ids = pool.get('cci.courriel.entrant').search(cr, uid, [('date_courriel','>=',date_debut), ('date_courriel', '<=', date_fin)])
				for ce in ce_ids:
					ref = self.pool.get('cci.courriel.entrant').browse(cr, uid, ce, context=context).ref_entrant
					date_courriel = self.pool.get('cci.courriel.entrant').browse(cr, uid, ce, context=context).date_courriel
					note_id = self.pool.get('cci.courriel.entrant').browse(cr, uid, ce, context=context).note_id
					type_id = self.pool.get('cci.courriel.entrant').browse(cr, uid, ce, context=context).type_id

					objet = self.pool.get('cci.courriel.entrant').browse(cr, uid, ce, context=context).objet
					name = self.pool.get('cci.courriel.entrant').browse(cr, uid, ce, context=context).name
					dept_id = self.pool.get('cci.courriel.entrant').browse(cr, uid, ce, context=context).dept_id.name
					data = {
						'ref': ref,
						'dateAuj': dateAuj,
						'date_courriel':date_courriel,
						'note_id':note_id,
						'type_id':type_id,
						'objet':objet,
						'name':name,
						'dept_id':dept_id,
					}
					result.append(data)
				print 'data..............',data


#######Etat#####


			if state and permanent != True: 
				etat_ids = pool.get('cci.courriel.entrant').search(cr, uid, [('state','=','draft')])
				print etat_ids
				for etat in etat_ids:
					ref = self.pool.get('cci.courriel.entrant').browse(cr, uid, etat, context=context).ref_entrant
					#date_courriel = self.pool.get('cci.courriel.entrant').browse(cr, uid, etat, context=context).date_courriel
					note_id = self.pool.get('cci.courriel.entrant').browse(cr, uid, etat, context=context).note_id
					type_id = self.pool.get('cci.courriel.entrant').browse(cr, uid, etat, context=context).type_id.name
					objet = self.pool.get('cci.courriel.entrant').browse(cr, uid, etat, context=context).objet
					name = self.pool.get('cci.courriel.entrant').browse(cr, uid, etat, context=context).name
					dept_id = self.pool.get('cci.courriel.entrant').browse(cr, uid, etat, context=context).dept_id.name
					data = {
						'ref': ref,
						'dateAuj': dateAuj,
						#'date_courriel':date_courriel,
						'note_id':note_id,
						'type_id':type_id,
						'objet':objet,
						'name':name,
						'dept_id':dept_id,
					}
					result.append(data)
				print 'data..............',data
			else :

				data = {
					'ref': '',
					'dateAuj': dateAuj,
					'date_courriel':'',
					'note_id':'',
					'type_id':'',
					'objet':'',
					'name':'',
					'dept_id':'',
                        		#'stat_path' :os.getcwd()+"/openerp/addons/reporting/",
				}
				result.append(data)

		
		print 'result..............',result
				
		return result
		
jasper_report.report_jasper('report.jasper_fiche_courriel_entrant_print', 'cci.courriel.entrant', parser=jasper_client, )
