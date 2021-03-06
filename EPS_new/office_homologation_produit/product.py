# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################



import time



from openerp import api, tools, SUPERUSER_ID
from openerp.osv import osv, fields, expression
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


import openerp.addons.decimal_precision as dp






class product_category_douane(osv.osv):
    _name = "product.category.douane"
    #_inherit = "product.category"



    _columns = {

	
        'name': fields.char('Nom',required=True),
        'designation': fields.char('Désignation'),
        'category_lines': fields.one2many('product.category.douane.line', 'categorie_id', ' '),
        'coeff_rev': fields.float('Coeff rev', digits_compute= dp.get_precision('Product Price'),readonly=True),      


    }
    
    
    def button_add_frais(self, cr, uid, ids, context=None):
    	print "heloo "
    	categ_line = self.pool.get('product.category.douane.line')
    	frais_ids = self.pool.get('frais.var.produit').search(cr, uid, [])
    	frais_obj = self.pool.get('frais.var.produit').browse(cr, uid,frais_ids)
    	if frais_obj:
    		for frais in frais_obj:
    			vals={
    				'frais_id':frais.id,
    				'taux':'0%',
    				'categorie_id':ids[0],
    			}
    			categ_line.create(cr,uid,vals)
    			

product_category_douane()


class product_category_douane_line(osv.osv):

    _name = "product.category.douane.line"

    _columns = {
        'categorie_id' : fields.many2one('product.category.douane' , 'categorie' , ondelete='cascade',invisible=True),
        'frais_id': fields.many2one('frais.var.produit','Frais', ondelete='restrict',readonly=True),
        'taux': fields.char('Taux'),




    }
    
    
    
class product_template(osv.osv):

    _name = 'product.template'
    _inherit = 'product.template'
    _columns = {

		'categ_douane_id': fields.many2one('product.category.douane', 'Catégorie douane', ondelete='cascade'),
    }

product_template()





