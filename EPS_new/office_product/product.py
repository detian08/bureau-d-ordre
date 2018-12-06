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

import string
import re
from openerp.osv import osv, fields, expression
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp import api
from openerp.exceptions import ValidationError

class product_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'



    _columns = {

        #rim modif 14/04/2014
        #'fodec':fields.boolean('FODEC'),
        'default_code' : fields.char('Internal Reference', select=True,required=True),
                # lot product fields

    }




product_product()


class product_supplierinfo(osv.osv):

    @api.one
    @api.depends('prix', 'rate','currency_id')
    def _amount_line(self):
        '''
           Methode qui permet de calculer le sous total d'une ligne de devis
        '''
        if self.currency_id:
            self.price_subtotal = self.prix / self.rate

    _name = 'product.supplierinfo'
    _inherit = 'product.supplierinfo'
    _columns = {
        'prix': fields.float("Prix d'achat",digits_compute=dp.get_precision('Account'), required=True),
        'currency_id': fields.many2one('res.currency', 'Currency', required=True),
        'supplier_discount':fields.float('Remise'),
        'price_subtotal': fields.float(string='Prix Monnaie Locale', digits= dp.get_precision('Account'),
        store=True, compute='_amount_line'),
    'rate': fields.float('rate',digits_compute=dp.get_precision('Account')),
    'min_qty': fields.float('Minimal Quantity',  help="The minimal quantity to purchase to this supplier, expressed in the supplier Product Unit of Measure if not empty, in the default unit of measure of the product otherwise."),
    'delay' : fields.integer('Delivery Lead Time',  help="Lead time in days between the confirmation of the purchase order and the receipt of the products in your warehouse. Used by the scheduler for automatic computation of the purchase order planning."),


    }

    def currency_id_change(self, cr, uid, ids, currency, context=None):
        res_final = {}
        if currency:
                #les informations sur le produit
            currency_obj = self.pool.get('res.currency').browse(cr,uid,currency,context=context)
                #designation=product_obj.name_template
            rate = currency_obj.rate_silent
                #les informations sur les taxes du produit
                #taxes = self.pool.get('product.product').browse(cr,uid,product,context=context)

            res_final = {'value':{'rate':rate}}
        return res_final

product_supplierinfo()


class product_template(osv.osv):
    _name = 'product.template'
    _inherit = 'product.template'

    # def _check_length(self, cr, uid, ids, context=None):
    #
    #     print "==============1", self.browse(cr, uid, ids, context=context).name
    #     for partner in self.browse(cr, uid, ids, context=context):
    #         print "==============2", self.browse(cr, uid, ids, context=context).name
    #
    #         if (len(self.browse(cr, uid, ids, context=context).name)) >= 5:
    #             print "==============3", self.browse(cr, uid, ids, context=context).name
    #
    #             return False
    #     return True
    #
    # _constraints = [
    #     (_check_length, ' Nom du produit trop long!', ['name'])
    # ]

    #     name = vals.get('name')
    #     print '============ name create', name

    # def write(self, cr, user, ids, vals, context=None):
    #     print '=============',vals
    #     name=vals.get('name')
    #     print '============ name write',name
    #     for partner in self.browse(cr, user, ids, context=context):
    #         new_name = self.browse(cr, user, ids, context=context)
    #         if (len(new_name.name)) >= 5:
    #             print "==============3", new_name.name
    #             raise osv.except_osv(_('Paramètre(s) incorrecte(s)!'),
    #                            _('Vérifier les codes à barre du produit et son bon de commande'))
    #
    #         else :
    #             print '==============eror'
    #     res = super(product_template, self).write(cr, user, ids, vals, context=context)
    #
    #     return res
########Commentaire MarouaT######
#    def _get_lot_id(self, cr, uid, ids, name, arg, context=None):
#        res = {}
#        prod=self.browse(cr, uid, ids)
#        print "*********************************************************",prod
#        for id in ids:
#            print "+++++++++++++++++++++",id
#            lot_id = self.pool.get('product.compose.line').search(cr, uid, [('lot_product_id', '=', id)])
#            if lot_id:
#                parent=self.pool.get('product.compose.line').browse(cr, uid, lot_id[0]).product_parent_id
#                print "aaaaaaaaaaaaaaaaaaaa",lot_id
#                print "parent***********",parent.id
#                #res[id] = lot_id and lot_id[0] or None
#                res[id] =parent.id
#        return res
########Commentaire MarouaT######
    def _compute_readonly_true(self, cr, uid, ids, field_name, arg, context=None):
        user_id=self.pool.get('res.users').browse(cr,uid,uid,context=context).id

        group_sale_ids = self.pool.get('res.groups').search(cr, uid, [('name','=','Responsable Vente')])
        group_sale_id = self.pool.get('res.groups').browse(cr, uid, group_sale_ids, context=context).id

        group_purchase_ids = self.pool.get('res.groups').search(cr, uid, [('name','=','Responsable Achat')])
        group_purchase_id = self.pool.get('res.groups').browse(cr, uid, group_purchase_ids, context=context).id

        res = {}
        list_gid=[]
        for id in ids:
            cr.execute('SELECT gid FROM res_groups_users_rel WHERE uid = %s',(user_id,))
            lines = cr.dictfetchall()

            for line in lines :
                gid=line['gid']
                list_gid.append(gid)

            if (group_sale_id in list_gid) and (group_purchase_id not in list_gid)  :
                res[id] = True
            elif (group_sale_id in list_gid) and (group_purchase_id in list_gid):
                res[id] = False
        return res


    _columns = {
        ##marR##'affichage': fields.boolean('Pour affichage'),
        'purchase_price': fields.float('Prix de revient', digits_compute=dp.get_precision('Product Price')),
        'default_code': fields.related('product_variant_ids', 'default_code', type='char', string='Internal Reference',required=True),
        'is_lot': fields.boolean('Lot des produits'),
        'readonly_true': fields.function( _compute_readonly_true, type="boolean"),
        ##marR##'lot_qty': fields.integer('Quantity products in Lot'),
        ##marR##'lot_product_id': fields.many2one('product.product', 'Product in lot'),  # In fact is one2one

########Commentaire MarouaT######
#        'lot_product_ids': fields.one2many('product.compose.line','product_parent_id' ,'Product in lot'),

        # normal product fields
#        'lot_id': fields.function(_get_lot_id, type='many2one', relation='product.template', string='Utilisé dans le Lot')
########Commentaire MarouaT######

    }



    _defaults = {
        'purchase_price': 1,
        'type' : 'product',
        'is_lot': False
    }

    def create(self, cr, uid, vals, context=None):
        #product_template_id = super(product_template, self).create(cr, uid, vals, context=context)
        user_id=self.pool.get('res.users').browse(cr,uid,uid,context=context).id

        group_sale_ids = self.pool.get('res.groups').search(cr, uid, [('name','=','Responsable Vente')])
        group_sale_id = self.pool.get('res.groups').browse(cr, uid, group_sale_ids, context=context).id

        group_purchase_ids = self.pool.get('res.groups').search(cr, uid, [('name','=','Responsable Achat')])
        group_purchase_id = self.pool.get('res.groups').browse(cr, uid, group_purchase_ids, context=context).id

        res = {}
        list_gid=[]

        cr.execute('SELECT gid FROM res_groups_users_rel WHERE uid = %s',(user_id,))
        lines = cr.dictfetchall()

        for line in lines :
            gid=line['gid']
            list_gid.append(gid)

        if (group_sale_id in list_gid) and (group_purchase_id not in list_gid)  :
            raise ValidationError(u"Vous n'avez pas l'accès de créer un article ! Veuillez consultez l'adminstrateur")
            #product_template_id = super(product_template, self).create(cr, uid, vals, context=context)

        else:
            return super(product_template, self).create(cr, uid, vals, context=context)



product_template()


########Commentaire MarouaT######
#class product_compose_line(osv.osv):
#    _name = 'product.compose.line'
#    _columns = {
#        'lot_product_id': fields.many2one('product.template', 'Produit dans le lot'),
#        'lot_qty': fields.integer('Quantite du produits dans le Lot'),
#        'product_parent_id': fields.many2one('product.template', 'Produit Parent du lot'),
#    }
#product_compose_line()
########Commentaire MarouaT######


class product_category(osv.osv):
    _name = 'product.category'
    _inherit = 'product.category'

    def    _categorie_get(self, cr, uid, context=None):
        ids = self.pool.get('product.category').search(cr, uid, [('name', '=','All')], context=context)
        return ids[0]

    _columns = {
        'parent_id': fields.many2one('product.category','Parent Category', select=True, ondelete='cascade'),#,readonly=True
    }

    _defaults = {
           'parent_id':_categorie_get

    }
product_category()
