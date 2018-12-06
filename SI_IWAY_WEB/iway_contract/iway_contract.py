# -*- coding: utf-8 -*-

#from openerp.osv import fields, osv
#from openerp import models, fields, api
#from openerp import fields, models, api
from openerp.osv import osv
from openerp.osv import fields
import time

#from openerp import SUPERUSER_ID
#from openerp.osv import fields, osv


#import date
from datetime import datetime
from datetime import date
from datetime import timedelta
from openerp.osv import fields, osv
from openerp import tools


from openerp import api



class hr_contract(osv.osv):
	_inherit="hr.contract" #Contrats


	_columns = {
                 'salaire de base': fields.float('Salaire de base', digits=(16,2), required=True, help="Basic Salary of the employee"),
                 'salaire net': fields.float('salaire net', digits=(16,2), required=True, help="net salary of the employee"),
                 
		#'type': fields.selection( (('m','Poste'),('f','Pfe'),('s','spontanné')), 'Type'),
		#type  : offre, pfe, spontanné
		#'category_ids': fields.many2many('hr.employee.category', 'employee_category_rel', 'emp_id', 'category_id', 'Tags')
           	#'type_id': fields.Many2one('hr.applicant', 'user_id', 'Related employees'),
		#'My_new_fields': fields.char('My new fields', required=True),
                 #entretien_ids : fields.one2many(string="entretiens" , comodel_name="iway_entretien.iway_entretien" , inverse_name="candidature_id"),	
                #'entretien_ids' : fields.one2many('iway_entretien.iway_entretien', 'candidature_id', 'Entretiens'),	    



    
}

	
