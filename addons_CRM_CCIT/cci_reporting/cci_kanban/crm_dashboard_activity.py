#-*- coding:utf-8 -*-
import json
import time
from datetime import date, datetime, timedelta
import calendar
from babel.dates import format_datetime, format_date
from openerp import models, api, _, fields


class crm_dashboard_activity(models.Model):
    _name = "crm.dashboard.activity"

    @api.one
    def _kanban_dashboard(self):
        self.kanban_dashboard = json.dumps(self.get_journal_dashboard_datas())


    @api.one
    def _dashboard_activity(self):
		self.dashboard_activity = json.dumps(self.get_dashboard_activity())
    @api.one
    def _dashboard_activity_appel(self):
		self.dashboard_activity_appel = json.dumps(self.get_dashboard_activity_appel())
    @api.one
    def _dashboard_activity_reunion(self):
		self.dashboard_activity_reunion = json.dumps(self.get_dashboard_activity_reunion())
    @api.one
    def _dashboard_activity_consultation(self):
		self.dashboard_activity_consultation = json.dumps(self.get_dashboard_activity_consultation())


    name = fields.Char(string='Name') 
    type_dash = fields.Selection([('activity', "activity"),('appel',"appel"),('reunion',"reunion"),('consultation',"consultation")])

    kanban_dashboard = fields.Text(compute='_kanban_dashboard')

    dashboard_activity = fields.Text(compute='_dashboard_activity')
    dashboard_activity_appel = fields.Text(compute='_dashboard_activity_appel')
    dashboard_activity_reunion = fields.Text(compute='_dashboard_activity_reunion')
    dashboard_activity_consultation = fields.Text(compute='_dashboard_activity_consultation')


    show_on_dashboard = fields.Boolean(string='Show journal on dashboard', help="Whether this journal should be displayed on the dashboard or not", default=True)


    @api.multi
    def get_journal_dashboard_datas(self):
	print ''


    ##Nombre d'email envoyé par activité
    @api.multi
    def get_dashboard_activity(self):
	data = []
	list_prod = []
	list_opportunity = []
	list_section = []
	list_opportunity_chef = []
	list_opportunity_comm = []
	list_section_comm = []

	if self.type_dash == 'activity' :
		user_id = self.env['res.users'].browse(self.env.uid).id ##user en cours
		##Liste des produits à suivre
		product_ids = self.env['product.template'].search([('a_suivre','=',True),('state','=','validate')])
		print 'product_ids........',product_ids
		if product_ids :
			for product in product_ids :
				list_prod.append(product.id)
	
		opportunity_ids = self.env['crm.lead'].search([('product_id','in',tuple(list_prod))])
		if opportunity_ids:
			for opportunity in opportunity_ids :
				list_opportunity.append(opportunity.id)
			print 'list_opportunity........',list_opportunity ##pour l'administrateur


#######################le mail###########################" 

		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id),('active','=','True')])
		print 'section_ids........',section_ids
		if section_ids:
			for section in section_ids:
				list_section.append(section.id)

		if list_opportunity and user_id == 1:
			#pour l'administrateur
			##pour email
			self.env.cr.execute("SELECT COUNT(m.id), mail_message_id FROM mail_mail m WHERE state =%s AND opportunity_ids in %s GROUP BY mail_message_id",("sent",tuple(list_opportunity)))

			res = self.env.cr.dictfetchall()
			print 'res .......',res
			for i in res:
				mail_id = i['mail_message_id']
				nb_mail = i.get('count')
				print "nb_mail",nb_mail
				# self.env.cr.execute("SELECT subject FROM mail_message WHERE id =%s",(mail_message_id,))
				# result = self.env.cr.dictfetchall()
				# print "result",result



				data.append({'label':mail_id , 'value':nb_mail,'id':self.id})
			return [{'values': data, 'area': True,'id': self.id}]
				

####################################################appel ##########################"""""
    ##Nombre d'appel par activité
    @api.multi
    def get_dashboard_activity_appel(self):
	data = []
	list_prod = []
	list_opportunity = []
	list_section = []
	list_opportunity_chef = []
	list_opportunity_comm = []
	list_section_comm = []

 	if self.type_dash == 'appel':
		
##################################ADMINISTRATEUR################################"

		#if user_id == 1:
			#pour l'administrateur

			##pour appelself.env.cr.execute('SELECT COUNT(c.id), default_code, p.id FROM crm_lead c, product_product p where c.product_id = p.product_tmpl_id AND c.stage_id IN %s AND product_id IN %s GROUP BY (default_code,p.id)',((6,7),tuple(list_prod)))


			self.env.cr.execute('SELECT COUNT(c.id), p.name, r.id, p.id FROM crm_phonecall c, res_users r, res_partner p WHERE c.user_id = r.id AND r.partner_id=p.id GROUP BY (p.name,r.id,p.id)')
#select name, user_id from calendar_event group by (name,user_id) ;

			#self.env.cr.execute("SELECT COUNT(c.id), name FROM crm_phonecall c WHERE state =%s GROUP BY name",("open",))





			res = self.env.cr.dictfetchall()
			print 'res .......',res
			for i in res:
				appel_id = i['name']
				nb_appel = i.get('count')
			        print 'nb_appel .......',nb_appel
				data.append({'label':appel_id , 'value':nb_appel,'id':self.id})

			return [{'values': data, 'area': True, 'id': self.id}]

##############################reunion###########################"

    ##Nombre de réunion par activité
    @api.multi
    def get_dashboard_activity_reunion(self):
	data = []
	list_prod = []
	list_opportunity = []
	list_section = []
	list_opportunity_chef = []
	list_opportunity_comm = []
	list_section_comm = []

 	if self.type_dash == 'reunion' :
		
				 
##################################ADMINISTRATEUR################################"

		#if list_opportunity and user_id == 1:
			#pour l'administrateur

			##pour réunion
			#self.env.cr.execute('SELECT COUNT(e.id), e.name FROM calendar_event e  GROUP BY (e.name,e.id)')
			#self.env.cr.execute("SELECT COUNT(e.id), name FROM calendar_event e WHERE opportunity_ids in %s GROUP BY name",(tuple(list_opportunity),))

			self.env.cr.execute('SELECT COUNT(e.id), p.name, r.id, p.id FROM calendar_event e, res_users r, res_partner p WHERE e.user_id = r.id AND r.partner_id=p.id GROUP BY (p.name,r.id,p.id)')

			res = self.env.cr.dictfetchall()
			print 'res....',res
			for i in res:
				reunion_id = i['name']
				nb_reunion = i.get('count')
				print "nb_reunion",nb_reunion
				data.append({'label':reunion_id , 'value':nb_reunion,'id':self.id})
			return [{'values': data, 'area': True,'id': self.id}]



		



##############################consultation###########################"

    ##Nombre de consultation par activité
    @api.multi
    def get_dashboard_activity_consultation(self):
	data = []
	list_prod = []
	list_opportunity = []
	list_section = []
	list_opportunity_chef = []
	list_opportunity_comm = []
	list_section_comm = []

 	if self.type_dash == 'consultation' :
		
				 
##################################ADMINISTRATEUR################################"

		#if list_opportunity and user_id == 1:
			#pour l'administrateur

			##pour réunion
			#self.env.cr.execute('SELECT COUNT(e.id), e.name FROM calendar_event e  GROUP BY (e.name,e.id)')
			#self.env.cr.execute("SELECT COUNT(e.id), name FROM calendar_event e WHERE opportunity_ids in %s GROUP BY name",(tuple(list_opportunity),))

			##self.env.cr.execute('SELECT COUNT(e.id), p.name, r.id, p.id FROM calendar_event e, res_users r, res_partner p WHERE e.user_id = r.id AND r.partner_id=p.id GROUP BY (p.name,r.id,p.id)')

			self.env.cr.execute('SELECT COUNT(n.id), responsable, n.name  FROM cci_consultation n  GROUP BY (n.name,responsable)')


			res = self.env.cr.dictfetchall()
			print 'res....',res
			for i in res:
				consultation_id = i['responsable']
				nb_consultation = i.get('count')
				print "nb_consultation",nb_consultation
				data.append({'label':consultation_id , 'value':nb_consultation,'id':self.id})
			return [{'values': data, 'area': True,'id': self.id}]



		


