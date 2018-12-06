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



class hr_emplyee(osv.osv):
	_inherit="hr.employee" #emplyee


	_columns = {
 
		'sequence_id' : fields.char('Matricule',readonly=True),
		
		
		
}
	_defaults = {
		'sequence_id': lambda self,cr,uid,context={}: self.pool.get('ir.sequence').get(cr, uid, 'employee'),
}

