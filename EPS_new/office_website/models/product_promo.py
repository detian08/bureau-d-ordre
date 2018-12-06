from openerp import models, fields, api


class product_promo(models.Model):
	_name = 'product.promo'
	
	product_id = fields.Many2one(comodel_name='product.template',string="Article")
	price_revient = fields.Integer(string="Prix de vente")
	price_promo = fields.Integer(string="Prix de promotion")
	actif = fields.Boolean(string="Active")

	#get the price of the product 
	@api.onchange('product_id')# if these fields are changed, call method
	def on_change(self):
		price = self.env['product.template'].browse(self.product_id.id).list_price
		print "....price",price
		self.price_revient = price
		

    
