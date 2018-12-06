# -*- coding: utf-8 -*-

from datetime import date, datetime
from dateutil import relativedelta
from openerp import tools, api
from openerp.osv import fields, osv
from openerp.exceptions import Warning
from openerp.exceptions import except_orm

class op_eco_distance(osv.osv):
    _name="op.eco.distance"



    _columns = {
	'operator_id':fields.many2one('res.partner'),
	'demande_operator_id':fields.many2one('res.partner.request'),

    }
   
