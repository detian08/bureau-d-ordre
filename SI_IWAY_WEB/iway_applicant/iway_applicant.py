# -*- coding: utf-8 -*-
#from openerp.osv import fields, osv
#from openerp import models, fields, api
#from openerp import fields, models, api
from openerp.osv import osv
from openerp.osv import fields

#import date
from datetime import datetime
from datetime import date
from datetime import timedelta
from openerp.osv import fields, osv
from openerp import tools


from openerp import api



class hr_applicant(osv.osv):
	_inherit="hr.applicant" #CANDIDATURE


	_columns = {
 #(('poste','Poste'),('pfe','PFE'),('spontanne','Spontanné'))
		'type': fields.selection( (('m','Poste'),('f','Stage'),('s','spontanné')), 'Type'),
		'diplome': fields.char('Diplôme', required=True),
		'specialite': fields.char('Spécialité', required=True),
		'employeuractuel': fields.char('Employeur Actuel'),
		'annee': fields.date('Année',required=False),
		#'nbanneesmoisdexperience': fields.integer('Nb années/mois dexperience', required=True)
		
		

		#type  : offre, pfe, spontanné
		#'category_ids': fields.many2many('hr.employee.category', 'employee_category_rel', 'emp_id', 'category_id', 'Tags')
           	#'type_id': fields.Many2one('hr.applicant', 'user_id', 'Related employees'),
		'My_new_fields': fields.char('My new fields', required=True),
                 #entretien_ids : fields.one2many(string="entretiens" , comodel_name="iway_entretien.iway_entretien" , inverse_name="candidature_id"),	
                'entretien_ids' : fields.one2many('iway_entretien.iway_entretien', 'candidature_id', 'Entretiens'),
#universités_etablissement--#
		'university' : fields.many2one('category.university', 'Université'),
		'establishment' : fields.many2one('category.establishment', 'Établissement'),
		'sequence_id' : fields.char('Référence annonce Recrutement',readonly=True),
		'profil': fields.char('Profil', required=True),
                'stagiaire': fields.char('Stagiaire'),
		'cin': fields.char('Cin', required=True , size=8),

#<!--Workflow-->  
    #attendees_count = fields.Integer(string="Attendees count", compute='_get_attendees_count', store=True)
		'state' : fields.selection([
        ('soumise', "Soumise"),
        ('entretien', "Entretien"),
        ('contratpropose', "Contrat proposé"),
 	#('contrat signe', "Contrat signé"),
 	#('refuse', "Refusé"),
    ], default='soumise'),
		
}
	_defaults = {
		'sequence_id': lambda self,cr,uid,context={}: self.pool.get('ir.sequence').get(cr, uid, 'condidature'),
}
#cin
	#_constraints = [
     			#(_check_cin,
           	#'Le format du cin ne dépasse pas  8 Chiffres' ,
           		#['cin']),
			#]
 	#_sql_constraints = [
                     #('cin',
                    	#'len(str(self.cin)) > 8',
                     	#'Vérifier le nbre de chiffre de cin <8 !'),

			  #]
	def _check_cin(self, cr, uid, ids, context=None):
        	print ".................", self.cin
		print '..............',type(self.cin)
                if len(str(self.cin)) > 8:
               		raise Warning('The max is 8, you can not add the third!')
	#_sql_constraints = [
                    # ('cin',
                     #'unique(cin)',
                     #'Vérifier le cin- il existe déjà!'),

			  #]

#cin


	@api.multi
	def action_soumise(self):
		print 'hello soumise'
		self.state = 'soumise'

	@api.multi
	def action_entretienn(self):
		print 'hello entretienn'
		self.state = 'entretien'

	@api.multi
	def action_contratpropose(self):
		print 'hello contratpropose'
		self.state = 'contratpropose'


#methode d"envoi

	def send_notification(self, cr, uid, ids, context=None) :
		print "helooooo.............."
		obj = self.browse(cr, uid, ids)
		print "obj.....",obj
		print "ids.....",ids[0]
		entretien_obj=self.pool.get('iway_entretien.iway_entretien')

		#boucle for pour récupérer le responsable et la date de l'entretien
		for entretien_id in self.browse(cr,uid,ids,context=context).entretien_ids:
			print "entretien_id .......",entretien_id
			user = entretien_obj.browse(cr,uid,entretien_id.id,context=context).responsable
			print '..........',user #retour id du responsable (res.users)
			date_entretien = entretien_obj.browse(cr,uid,entretien_id.id,context=context).date_entretien
			print "date_entretien",date_entretien
			user_name = self.pool.get('res.users').browse(cr, uid, user.id, context=context).name
			print 'name ....',user_name
			user_email = self.pool.get('res.users').browse(cr, uid, user.id, context=context).email
			print 'email ....',user_email
			
            		

			mail_vals = {
				'body': '<html>Votre rendez-vous </html>',
				'record_name': 'Entretien',
				'res_id': ids[0],
				'reply_to': user_name,
				'author_id': user.id,
				'model': 'hr.applicant',
				'type': 'notification',
				'email_from':user_email,
				'starred': True,
				}
			print "mail_vals ......",mail_vals
			message = self.pool.get('mail.message').create(cr, uid, mail_vals)
			print "........",message
			mail_notif_vals = {
				'partner_id': self.pool.get('res.users').browse(cr, uid, user.id, context=context).partner_id.id,
				'message_id': message,
				'is_read': True,
				'starred': True,
			}
			print 'mail_notif_vals......',mail_notif_vals
			notif= self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)
#-----------------------------------calendar

			calendar_vals = {
				'name':'Entretien',
				'user_id': user.id,
				'start':date_entretien,
				'stop':date_entretien,
				}
			print "calendar_vals ......",calendar_vals
			calendar = self.pool.get('calendar.event').create(cr, uid, calendar_vals)
			
			print 'calendar......',calendar
		print "fin ........................"
		return True
		








