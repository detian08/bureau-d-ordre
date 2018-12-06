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



class hr_job(osv.osv):
	_inherit="hr.job" #postes


	_columns = {
 #(('poste','Poste'),('pfe','PFE'),('spontanne','Spontanné'))
		'type': fields.selection( (('r','Recrutement'),('t','Titre_Poste')), 'Type'),
		'site': fields.selection( (('s','Sfax'),('t','Tunis'),('m','manzeltmim')), 'Site'),
		#'diplome': fields.char('Diplôme', required=True),
		#'specialite': fields.char('Spécialité', required=True),
		#'employeuractuel': fields.char('Employeur Actuel'),
		#'annee': fields.date('Année',required=False),
		#'nbanneesmoisdexperience': fields.integer('Nb années/mois dexperience', required=True)
		
		

}

	
