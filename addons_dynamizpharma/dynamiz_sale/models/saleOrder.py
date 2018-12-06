# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models
import datetime

class saleOrder(models.Model):
    _inherit = "sale.order"

    def facturer(self):
        order_id = self.id
        print (order_id)
        for line in self.env['sale.order.line'].search([('order_id', '=', order_id)]):
            print (line)

        product_id = self.env['sale.order.line'].browse(line.id).product_id.id  ##product.product
        product_tmpl_id = self.env['product.product'].browse(product_id).product_tmpl_id.id
    # for comp_id in self.env['product.product'].browse(product_id).compIds
        for comp_id in self.env['product.template'].browse(product_tmpl_id).co_ids:
            print (comp_id)
            #fournisseur = self.env['composant'].browse(comp_id.id).fournisseur.id
             fournisseur= self.env['product.supplierinfo'].browse(name).saller_ids

  ##suppliers = self.env['product.supplierinfo'].search([
                    #('name', '=', self._context.get('partner_id')),
            prix = self.env['composant'].browse(comp_id.id).prix
            quantite = self.env['composant'].browse(comp_id.id).quantite

            print ("le fournisseur est:",fournisseur)
            print ("le prix est:",prix)
            print ("a quantite est:", quantite)
##dict tuple list
            vals = {
                'date_order': datetime.datetime.now(),#date du jour
                'name': 'name',
                'partner_id': fournisseur
            }
            purchase_id= self.env['purchase.order'].create(vals)#bc achat

            datePurchase=self.env['purchase.order'].browse(purchase_id.id).date_order
            prod=self.env['composant'].browse(comp_id.id).article
            unite = self.env['sale.order.line'].browse(line.id).product_uom.id
            print("unite", unite)

            comp_vals = {
                'date_planned': datePurchase,
                'name': 'name',
                'price_unit':prix,
                'product_id':prod.id,
                'product_qty': quantite,
                'product_uom': unite,
                'partner_id': fournisseur,
                'order_id' :purchase_id.id,
		'state':'purchase',
            }

            res= self.env['purchase.order.line'].create(comp_vals)
