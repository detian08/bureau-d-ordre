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

		pool = pooler.get_pool(cr.dbname)
		result = []
		if 'form' in data:
			dateAuj = time.strftime('%d-%m-%Y')

			departement_id = data['form']['departement_id'][1]
			date1 = data['form']['date1']
			date2 = data['form']['date2']

			case_section_ids = pool.get('crm.case.section').search(cr, uid, [('name', '=', departement_id)])
			case_section_objs = pool.get('crm.case.section').browse(cr, uid, case_section_ids)

			case_section_name = case_section_objs[0].name
			print "case_section_name..............",case_section_name
			lead_ids = pool.get('crm.lead').search(cr, uid, [('section_id', '=', departement_id),
																 ('date_debut', '>=', date1),
																 ('date_fin', '<=', date2)
																 ])
			lead_objs = pool.get('crm.lead').browse(cr, uid, lead_ids)


#----------------Nombre des commerciaux
			cr.execute("SELECT member_id FROM sale_member_rel WHERE section_id =" + repr(case_section_objs[0].id))
			nb_com = len(cr.fetchall())

			nb_ops_gan = 0
			nb_ops_per = 0
			total_rev_gan = 0
			total_rev_per = 0
			nb_ops = 0

			date_deb = datetime.datetime.strptime(date1, "%Y-%m-%d").strftime('%d-%m-%Y')
			date_fin = datetime.datetime.strptime(date2, "%Y-%m-%d").strftime('%d-%m-%Y')

			if lead_objs:
				for lead in lead_objs:

					if lead.stage_id.name == "Won":
						nb_ops_gan = nb_ops_gan + 1
						total_rev_gan = total_rev_gan + lead.planned_revenue

					if lead.stage_id.name == "Lost":
						nb_ops_per = nb_ops_per + 1
						total_rev_per = total_rev_per + lead.planned_revenue

				nb_ops = nb_ops_gan + nb_ops_per


				data = {
					'dateAuj': dateAuj,
					'name': case_section_name,
					'date_deb': date_deb,
					'date_fin': date_fin,
					'nb_ops_gan': repr(nb_ops_gan),
					'total_rev_gan': repr(total_rev_gan) ,
					'nb_ops_per': repr(nb_ops_per),
					'total_rev_per': repr(total_rev_per) ,
					'nb_ops': repr(nb_ops),
					'nb_com': nb_com,
                                        'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",
				}
				result.append(data)

				cr.execute("SELECT DISTINCT user_id FROM crm_lead")

				users = cr.fetchall()

				for i in range(len(users)):
					cr.execute("SELECT DISTINCT(res_partner.name) FROM res_partner,res_users, crm_lead "
								"WHERE crm_lead.section_id = "+repr(case_section_objs[0].id) +
								"AND crm_lead.user_id = " + repr(users[i][0]) +
								"AND crm_lead.user_id = res_users.id "
								"AND res_users.partner_id = res_partner.id")
					user_name = cr.fetchall()

					com_lead_ids = pool.get('crm.lead').search(cr, uid,[('user_id', '=', users[i][0]),
																		('section_id', '=', departement_id),
																 		('date_debut', '>=', date1),
																 		('date_fin', '<=', date2)])
					com_lead_objs = pool.get('crm.lead').browse(cr, uid,com_lead_ids)

					if com_lead_objs:
						com_nb_op_gan = 0
						com_total_rev_gan = 0
						com_nb_op_per = 0
						com_total_rev_per = 0
						for lead in com_lead_objs:
							if lead.stage_id.name == "Won":
								com_nb_op_gan = com_nb_op_gan + 1
								com_total_rev_gan = com_total_rev_gan + lead.planned_revenue

							if lead.stage_id.name == "Lost":
								com_nb_op_per = com_nb_op_per + 1
								com_total_rev_per = com_total_rev_per + lead.planned_revenue
						com_nb_ops = com_nb_op_gan + com_nb_op_per

						data ={
							'com_nom': user_name[0][0],
							'com_nb_op': repr(com_nb_ops),
							'com_nb_op_gan':repr(com_nb_op_gan),
							'com_nb_op_per':repr(com_nb_op_per),
							'com_total_rev_gan':repr(com_total_rev_gan) ,
							'com_total_rev_per':repr(com_total_rev_per) ,
                                                        'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",
						}
						result.append(data)

			else:
				data = {
					'date_deb': date_deb,
					'date_fin': date_fin,
					'dateAuj': dateAuj,
					'name': case_section_name,
					'nb_ops_gan': repr(nb_ops_gan),
					'total_rev_gan': repr(total_rev_gan),
					'nb_ops_per': repr(nb_ops_per),
					'total_rev_per': repr(total_rev_per),
					'nb_ops': repr(nb_ops),
					'nb_com': repr(nb_com),
                                        'stat_path' :os.getcwd()+"/openerp/addons/cci_stat/",
				}
				result.append(data)



		return result


jasper_report.report_jasper('report.jasper_perform_dep_print', 'crm.case.section', parser=jasper_client, )
