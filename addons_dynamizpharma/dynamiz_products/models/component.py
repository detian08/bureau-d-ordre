# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models
class product_component(models.Model):
	_name = "product.component"

	#inverse de one2many
	product_id = fields.Many2one('product.template', string="Product", ondelete='cascade', index=True)
	quantity = fields.Integer(string='Quantity', translate=True)
	# fournisseur = fields.Many2one('res.partner', string='Fournisseur', translate=True)
	price = fields.Float(string='Price', translate=True)
	article = fields.Many2one('product.product', string="Article", ondelete='cascade', index=True)







