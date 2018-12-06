# -*- encoding: utf-8 -*-
import JasperDataParser
from openerp.jasper_reports import jasper_report
from openerp import pooler
import time
import datetime
import os

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
		uid = 1
		pool = pooler.get_pool(cr.dbname)
		result = []
		revenue_total = 0
		total_participant = 0
		if 'form' in data:

			product_id = data['form']['product_id'][1]
			#debut = data['form']['debut']
			#fin = data['form']['fin']


			#d_deb = datetime.datetime.strptime(debut, "%Y-%m-%d").strftime('%d-%m-%Y')
			#d_fin = datetime.datetime.strptime(fin, "%Y-%m-%d").strftime('%d-%m-%Y')

			#id_prod = data['form']['product_id'][0]
			dateAuj = time.strftime('%d-%m-%Y')

            # --------------------------Liste des secteurs d'activités
			#product = pool.get('product.template').search(cr, uid, [('name', '=', product_id)])
			#print "product.......",product
			#product_objs = pool.get('product.template').browse(cr, uid, product)
			#print "",product_objs
			#secteurs_ids =  pool.get('product.template').browse(cr, uid, product).product_sector_ids
			#if secteurs_ids:
			#	for secteur in secteurs_ids:
					
			#		print 'secteurs_ids.....................',secteur
			#		data = {
			#			'secteur_activity':secteur.id,
			#		}
			#		result.append(data)
			#else:
			#	data = {
			#			'secteur_activity':'',
			#	}
			#	result.append(data)

			# ----------------------------date de debut et date fin
			reg_ids = pool.get('product.template').search(cr, 1, [('name', '=', product_id)])
			reg_objs = pool.get('product.template').browse(cr, 1, reg_ids)

			# ----------------------------currency
			company_id = pool.get('res.company').search(cr,1,[])
			currency_id = pool.get('res.company').browse(cr,1,company_id).currency_id.id
			currency_name = pool.get('res.currency').browse(cr,1,currency_id).name


			if reg_objs:

				for reg in reg_objs:
					
					date_debut_prod = datetime.datetime.strptime(reg.date_debut, "%Y-%m-%d").strftime('%d-%m-%Y')
					date_fin_prod = datetime.datetime.strptime(reg.date_fin, "%Y-%m-%d").strftime('%d-%m-%Y')

					category_id =  pool.get('product.template').browse(cr, 1, reg.id).categ_id.id

					categ_name = pool.get('product.category').browse(cr, 1, category_id).name
					planned_revenue =  pool.get('product.template').browse(cr, 1, reg.id).list_price

					
					data = {
						'prod_date_deb':date_debut_prod,
						'prod_date_fin':date_fin_prod,
						'planned_revenue':planned_revenue,
						'currency_name':currency_name,
						'category_id':categ_name,
						'product_id': product_id,
						'dateAuj': dateAuj,
                        'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",
					}
					result.append(data)

			else:
				
				data = {
					'prod_date_deb':'',
					'prod_date_fin':'',
					'planned_revenue':'',
					'currency_name':'',
					'product_id': product_id,
					'category_id':'',
					'dateAuj': dateAuj,
                    'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",
				}
				result.append(data)

			# -----------------------------liste des participants
			participant_ids = pool.get('participant.contact').search(cr, 1, [('product_id', '=', reg_objs.id)])
			participant_objs = pool.get('participant.contact').browse(cr, 1, participant_ids)
			total_participant = 0
			if participant_objs:
				for par in participant_objs:
					total_participant = total_participant + 1

					data = {
						'name': par.name["name"],
						'participant_id': par.participant_id["name"].name,
                        'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",
					}
					result.append(data)

			

		# 	# -----------------------------liste des présences
			presence_ids = pool.get('session.presence').search(cr, 1, [])
			presence_objs = pool.get('session.presence').browse(cr, 1, presence_ids)
			if presence_objs:

				for pre in presence_objs:
					contact_id = pre.contact_id
					session_id = pre.session_id

					cr.execute("SELECT * FROM participant_contact WHERE id =%s", (contact_id.id,))
					lines = cr.dictfetchall()
					for line in lines:
						name = line['name']

						cont = pool.get('res.partner').browse(cr, 1, name).name

						cr.execute("SELECT * FROM product_session WHERE id =%s", (session_id.id,))
						lines = cr.dictfetchall()
						for line in lines:
							id = line['id']

						session_name = pool.get('product.session').browse(cr, 1, id).name

						data = {
							'contact_id': cont,
							'session_id': session_name,
							'dateAuj': dateAuj,
                        	'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",
						}

						result.append(data)
			else:
				data = {
					'dateAuj': dateAuj,
					'contact_id': '',
					'session_id': '',
                    'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",
				}
				result.append(data)

			# ------------------------revenue realisé
			crm_ids = pool.get('crm.lead').search(cr, 1, [('product_id', '=', reg_objs.id)])
			crm_objs = pool.get('crm.lead').browse(cr, 1, crm_ids)

			if crm_objs:
				for opp in crm_objs:
					if opp.stage_id.name == "Won":
						revenue_total = revenue_total + opp.planned_revenue
					data = {
						'revenue_total': revenue_total,
                        'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",
					}
					result.append(data)

			# -----------------------------liste des sessions-------------------------
			session_ids = pool.get('product.session').search(cr, 1, [('product_id', '=', reg_objs.id)])
			session_objs = pool.get('product.session').browse(cr, 1, session_ids)
			if session_objs:
				for session in session_objs:
					date_deb_ses = datetime.datetime.strptime(session.heure_debut, "%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y %H:%M')
					date_fin_ses = datetime.datetime.strptime(session.heure_fin, "%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y %H:%M')

					data = {
						'titre_ses': session.name,
						'date_deb_ses': date_deb_ses,
						'date_fin_ses': date_fin_ses,
                        'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",
					}
					result.append(data)



				# ---------------------liste des reclamations----------------------
			claim_ids = pool.get('crm.claim').search(cr, 1, [('product_id', '=', reg_objs.id)])
			claim_objs = pool.get('crm.claim').browse(cr, 1, claim_ids)

			if claim_objs:
				print 'claim_objs......',claim_objs
				for claim in claim_objs:

					if claim.state == 'soumise':
						state = 'Soumise'
					if claim.state == 'draft':
						state = 'Brouillon'
					if claim.state == 'validate':
						state = 'Traitée'
					if claim.state == 'reject':
						state = 'Rejetée'
					if claim.state == 'close':
						state = 'Cloturée'

					data = {
						'objet': claim.name,
						'partner': claim.partner_id["name"],
						'date_reclamation': claim.date,
						'echeance': claim.date_deadline,
						'responsable': claim.user_id["name"],
						'state': state,
                        'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",
					}
					result.append(data)

		# -----------------------------------

		data = {
			'revenue_total': repr(revenue_total),
			'total_participant': repr(total_participant),
            'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",
		}
		result.append(data)

		return result


jasper_report.report_jasper('report.jasper_fiche_product_print', 'crm.lead', parser=jasper_client, )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
