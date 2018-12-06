# -*- coding: utf-8 -*-
import werkzeug
#to inherit a controller 
from openerp.addons.website_sale.controllers.main import website_sale
from openerp.addons.website.controllers.main import Website

from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug
from openerp.addons.web.controllers.main import login_redirect

from openerp.addons.website_sale.controllers.main import QueryURL


class website_sale_inherit(website_sale):
	# @http.route(['/shop/cart'], type='http', auth="public", website=True)
	# def cart(self, **post):
	# 	cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
	# 	# res = super(website_sale_inherit, self).cart()
	# 	# print '',res
	# 	order = request.website.sale_get_order()
	# 	order_id = order.id
	# 	for line in http.request.env['sale.order.line'].search([('order_id','=',order_id)]):
	# 		product_id = http.request.env['sale.order.line'].browse(line.id).product_id
	# 		product_tmpl_id = http.request.env['product.product'].browse(product_id.id).product_tmpl_id.id
	# 		print '.....',product_tmpl_id
	# 		http.request.env.cr.execute('SELECT tax_id FROM product_taxes_rel WHERE prod_id =%s', (product_tmpl_id,))
	# 		taxes_id = http.request.env.cr.fetchall()
	# 		if taxes_id:
	# 			for tax in taxes_id:
	# 				tax_id = tax[0]
	# 				print 'tax_id',tax_id
	# 	amount_tax = 0
	# 	return super(website_sale_inherit, self).cart()

	@http.route(['/shop/product/<model("product.template"):product>'],type='http', auth="public", website=True)
	def product(self, product, category='', search='', **kwargs):
		cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
		print " ..........shop product............"
		#sum of the qty of a product
		qty = 0

		product_id = product.id
		# procuct_obj= http.request.env['product.template']
		# public_price = procuct_obj.browse(product_id).lst_price
		# context['pricelist'] = public_price

		#####afficher TVA
		tax_obj = http.request.env['account.tax']
		http.request.env.cr.execute('SELECT tax_id FROM product_taxes_rel WHERE prod_id =%s',(product_id,))
		taxes_id = http.request.env.cr.fetchall()
		if taxes_id :
			for tax in taxes_id :
				tax_id = tax[0]
			#tva = tax_obj.browse(tax_id).name
			tva = tax_obj.browse(tax_id).description
			context['tva'] = tva

		#####afficher qté
		stock = http.request.env['stock.quant']
		qty_product_id = stock.search([('product_id','=',product_id)])
		for qty_id in qty_product_id :
			qty += stock.browse(qty_id.id).qty
		context['quantity'] = qty

		#to inhertit a method of a controller
		return super(website_sale_inherit, self).product(product, category='', search='', **kwargs)
        	#return request.website.render("website_sale.product", values)

	@http.route([
		'/shop',
		'/shop/page/<int:page>',
		'/shop/category/<model("product.public.category"):category>',
		'/shop/category/<model("product.public.category"):category>/page/<int:page>'
	], type='http', auth="public", website=True)
	def shop(self, page=0, category=None, search='', **post):
		cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
		print " ..........shop catalogue............"

		tax_obj = http.request.env['account.tax']
		tax_ids = tax_obj.search([])
		print "....tax",tax_ids
		if tax_ids:
			for tax in tax_ids :
				context['tva'] = tax_obj.browse(tax.id).description

		# procuct_obj= http.request.env['product.template']
		# product_ids = procuct_obj.search([])
		# if product_ids :
		# 	for product_id in product_ids:
		# 		public_price = procuct_obj.browse(product_id.id).public_price
		# 		context['pricelist'] = public_price
		# print 'context .......',context
		# print 'page .......',page
		# print 'category .......',category
		return super(website_sale_inherit, self).shop(page,category, search, **post)



class WebsiteSlides(Website):
	@http.route('/', type='http', auth="public", website=True)
	def index(self, **kw): 
		request.context
		page = 'homepage'

		#les slides
		slides = http.request.env['slide.image']
		request.context['slides']=slides.search([])

		#Les produits actifs qui sont en promo
		promo_obj = http.request.env['product.promo']
		product = promo_obj.search([('actif','=',True)])
		request.context['product_promo'] = product

		#les catégories
		category_obj = http.request.env['product.public.category']
		category = category_obj.search([('parent_id', '=', False)])
		request.context['categories'] = category
        	keep = QueryURL('/page/category', category_id=[])
		request.context['keep'] = keep

		return super(WebsiteSlides, self).index()

##controlleur du newsletter qui permet d'enregistrer les emails dans la table des newsletter
class newsletter(http.Controller):
	@http.route('/newsletter/thankyou', methods=['POST'], type='http', auth="public", website=True)
	def newsletter_thankyou(self, **post):
		env = request.env()
		email = post.get('email')

		search_email = env['office.newsletter'].search([('email','=',email)])
		if not search_email :
			value = {'email' : email}
			newsletter_id = env['office.newsletter'].create(value).id
		return request.redirect('/')

class contact_us(http.Controller):
	@http.route('/thankyou', methods=['POST'], type='http', auth="public", website=True)
	def contact_thankyou(self, **post):
		mail_values = {
			"subject" :post.get('subject'),
			"body_html" :post.get('message'),
			"email_from" :post.get('email'),
			"email_to" :"marwa.benmessaoud@iway-tn.com",
		}
		email_id = request.env['mail.mail'].create(mail_values)
        	request.env['mail.mail'].send(email_id)

		return request.website.render('office_website.thankyou')
		#return request.redirect('/thankyou')

