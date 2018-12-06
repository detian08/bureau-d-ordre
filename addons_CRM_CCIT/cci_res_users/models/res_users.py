# -*- coding: utf-8 -*-

from datetime import date, datetime
from dateutil import relativedelta
from openerp import tools, api
from openerp.osv import fields, osv
from openerp.exceptions import Warning
from openerp.exceptions import except_orm
from pyjarowinkler import distance

class res_users(osv.osv):
    _inherit = 'res.users'

    _columns = {
	'a_suivre':fields.boolean(string="suivre"),

     
    }


