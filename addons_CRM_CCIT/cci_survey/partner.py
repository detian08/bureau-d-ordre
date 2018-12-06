# -*- coding: utf-8 -*-
from openerp import api
from openerp.tools.translate import _
from openerp.osv import fields, osv
from openerp.exceptions import Warning
from openerp.addons.web.http import request

class cci_partner(osv.Model):
    _name = 'res.partner'
    _inherit ='res.partner'

    def search_partner(self, cr, uid, vals, context=None):
	print 'vals.....',vals

  
        partner_obj = request.registry['res.partner']

	domain = [

	('name','=',vals.get('name')),
	('vat','=',vals.get('vat')),
	('email','=',vals.get('email')),
	('mobile','=',vals.get('mobile')),

	]



	partner_id = partner_obj.search(cr, uid,domain)
	#partner_id = self.pool.get('res.partner').search(cr, uid,[('name', '=', vals_name),('vat', '=', vals_vat),('email', '=', vals_email),('mobile','=', vals_mobile)])



 	print 'partner_id.....',partner_id


	return partner_id

