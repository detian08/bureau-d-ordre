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



class entretien_evaluation(osv.osv):
	_name = 'entretien_evaluation.entretien_evaluation'
	_description = "Evalutaion"

	_columns = {
 #(('poste','Poste'),('pfe','PFE'),('spontanne','Spontanné'))
		#'note': fields.selection( (('m','Poste'),('f','Pfe'),('s','spontanné')), 'Note'),
		'critere': fields.char('Critére', required=True),
		'note': fields.selection([('0','0%'),
                           ('25','25%'),
                           ('50','50%'),
                           ('75','75%'),
                           ('100','100%'),],
                            'Note', required=True),
		'entretien_id': fields.many2one('iway_entretien.iway_entretien', 'Evaluation', select=True),
		#'specialite': fields.char('Spécialité', required=True),
		#'employeuractuel': fields.char('Employeur Actuel'),
		#'annee': fields.date('Année',required=False),
		#'nbanneesmoisdexperience': fields.integer('Nb années/mois dexperience', required=True)
		
		

}

