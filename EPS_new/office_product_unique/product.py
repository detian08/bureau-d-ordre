# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api, _
from openerp.exceptions import Warning


class product_product(models.Model):
	_inherit = "product.product"

	@api.one
	@api.constrains('company_id', 'default_code')
	def check_unique_company_and_default_code(self):
		if  self.default_code and self.company_id:#self.active and
			filters = [
					   ('default_code', '=', self.default_code),
					   ('active', '=', True)
					   ]
			filters_1 = [
				       ('default_code', '=', self.default_code),
				       ('active', '=', False)
				       ]
				       #('active', '=', True) recherche aussi les produits inactifs
			prod_ids = self.search(filters)
			prod_idss = self.search(filters_1)


			if len(prod_ids) > 1 or prod_idss:
				raise Warning(
					_('Référence Interne existe déjà.'))

	@api.one
	@api.constrains('company_id', 'ean13')
	def check_unique_company_and_ean13(self):
		if  self.ean13 and self.company_id:#self.active and
			filters = [('company_id', '=', self.company_id.id),
					   ('ean13', '=', self.ean13)]
					   #, ('active', '=', True): recherche les produits inactifs
			prod_ids = self.search(filters)
			if len(prod_ids) > 1:
				raise Warning(
					_(' EAN code existe déjà !! '))
		
		            
                    
