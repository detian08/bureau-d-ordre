# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models , api



class product_template(models.Model):
    _inherit = "product.template"

    #prixpub = fields.Float(string='Prix pub', translate=True)



    component_ids = fields.One2many('product.component', 'product_id', string="Component", ondelete='cascade', index=True)

    #cltIds = fields.One2many('operator', 'cltid', string="clients", ondelete='cascade', index=True)


    # def stateProduct(self):
    #     produit=self.env['crm_lead'].stateTest().product
    #     print (produit)








