# -*- coding: utf-8 -*-

from datetime import date, datetime
from dateutil import relativedelta
from openerp import tools, api
from openerp.osv import fields, osv
from openerp.exceptions import Warning
from openerp.exceptions import except_orm
from pyjarowinkler import distance

class hr_emplyee(osv.osv):
    _inherit = 'hr.employee'

    _columns = {
	'present':fields.boolean(string="Présent"),

     
    }


