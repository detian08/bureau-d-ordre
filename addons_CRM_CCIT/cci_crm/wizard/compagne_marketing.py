# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime
from random import *
from itertools import cycle


class wizard_compagne(osv.osv_memory):
	_name = "wizard.compagne"###wizard.compagne
	_description = "Compagne Marketing"

	_columns = {
		'product_id': fields.many2one('product.template', "Produit"),
		'name': fields.many2one('res.partner.group', "Groupe"),
		'membres_ids': fields.many2many('res.users', 'res_user_compagne_rel', 'compagne_id', 'user_id', "Membres de l'équipe"),
		#'status':fields.float(""),
		# 'range_start' : fields.integer('Range From(%)', required=True,help="Starting range of Statusbar in Percentage"),
		# 'range_stop' : fields.integer('Range To(%)', required=True, help="Stop range of Statusbar in Percentage")
	}

	def get_opportunite(self, cr, uid, ids, context=None):

		list_op_eco = []
		list_members = []
		list_partners = []
		product_id = self.browse(cr, uid, ids, context=context).product_id.id
		product_price = self.pool.get('product.template').browse(cr,uid,product_id,context=context).list_price
		product_name = self.browse(cr, uid, ids, context=context).product_id.name

		groupe_id = self.browse(cr, uid, ids, context=context).name.id


		list_op_eco = self.pool.get('res.partner.group').browse(cr, uid, groupe_id,context=context).partner_ids


		#		vals = {
		#list_member = self.pool.get('res.users').browse(cr, uid, groupe_id,context=context)

		#section_id = self.pool.get('crm.case.section').search(cr, uid, [('member_ids','=',uid)],context=context)
		#print 'section_id .......',section_id
		#employee_id=self.pool.get('hr.employee').browse(cr, uid, uid, context=context).parent_id.id

		for op in list_op_eco:	

			id_partner = op.id
			email=self.pool.get('res.partner').browse(cr, uid, op.id,context=context).email
			tel=self.pool.get('res.partner').browse(cr, uid, op.id,context=context).mobile
			list_partners.append(id_partner)

		for id in list_partners :
			count=list_partners.count(id)
			if count > 1:
				list_partners.remove(id)

####liste memebres
		cr.execute('SELECT user_id FROM res_user_compagne_rel WHERE compagne_id=%s', (ids[0],))
		members = cr.fetchall()

		for member in members:

			member_id = member
			list_members.append(member_id)

			

		# ----------------------------------------------------------------

		crm_lead = self.pool.get('crm.lead')
		j = 0
		count=0
		for i in range(max((len(list_members), len(list_partners)))):

			try:
				#récupération du département du membre
				cr.execute('SELECT section_id FROM sale_member_rel WHERE member_id=%s', (list_members[i],))
				section_id = cr.fetchall()
				if section_id:
					vals = {
						'partner_id': list_partners[i],
						'type': 'opportunity',
						'user_id': list_members[i][0],
						'phone':tel,
						'email_from':email,
						'product_id': product_id,
						'section_id': section_id[0][0],
						'planned_revenue': product_price,
					}
				else:
					vals = {
						'partner_id': list_partners[i],
						'type': 'opportunity',
						'user_id': list_members[i][0],
						'phone':tel,
						'email_from':email,
						'product_id': product_id,
						# 'section_id': section_id[0][0],
						'planned_revenue': product_price,
					}
				count = count+1
				crm_lead.create(cr,uid,vals)
				print'yes......'
				self.write(cr, uid, ids,{'status':count})
			except IndexError:
				if len(list_partners) > len(list_members):
					# si la liste des membres (list_members) est términée, recommencer l'iteration sur cette liste pour
					# affecter les opérateurs économiques pour les opérateurs économiques (list_partners) restants
					restart = True
					while j < len(list_members) and restart:
						cr.execute('SELECT section_id FROM sale_member_rel WHERE member_id=%s', (list_members[j],))
						section_id = cr.fetchall()
						if section_id:
							vals = {
								'partner_id': list_partners[i],
								'type': 'opportunity',
								'user_id': list_members[j][0],
								'product_id': product_id,
								'section_id': section_id[0][0],
								'planned_revenue': product_price,
							}
						else:
							vals = {
								'partner_id': list_partners[i],
								'type': 'opportunity',
								'user_id': list_members[j][0],
								'product_id': product_id,
								#'section_id': section_id[0][0],
								'planned_revenue': product_price,
							}
						count = count + 1
						crm_lead.create(cr, uid, vals)
						print 'yes......'
						self.write(cr,uid,ids,{'status':count})

						# arreter la boucle sur la liste des membres (list_members) si la liste
						# des opérateurs économiques (list_partners) est terminée
						if i == len(list_partners) - 1:
							restart = False
						# recommencer la boucle si la fin de la liste des membres (list_members) est atteinte
						if j == len(list_members) - 1:
							j = 0

						# changer à chaque éxécution de la boucle, l'indice de l'itération,
						# pour pointer à chaque fois sur un membre
						else:
							j = j + 1

						# exécuter toujours une seule itération
						break
				elif len(list_partners) < len(list_members):
					break

		# return True
