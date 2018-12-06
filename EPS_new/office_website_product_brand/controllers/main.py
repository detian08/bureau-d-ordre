# -*- coding: utf-8 -*-

from openerp import http
from openerp.http import request
from openerp import SUPERUSER_ID
from openerp.addons.website_sale.controllers.main import QueryURL
from openerp.addons.website_sale.controllers.main import website_sale


class WebsiteSale(website_sale):

    @http.route(['/shop',
                 '/shop/page/<int:page>',
                 '/shop/category/<model("product.public.category"):category>',
                 """/shop/category/<model("product.public.category"):category>
                 /page/<int:page>""",
                 '/shop/brands',                 
		 '/shop/category'],
                type='http',
                auth='public',
                website=True)
    def shop(self, page=0, category=None, brand=None, search='', **post):
        if brand:
            request.context.setdefault('brand_id', int(brand))
        result = super(WebsiteSale, self).shop(page=page, category=category,
                                               brand=brand, search=search,
                                               **post)
	print "brand.........",brand
        result.qcontext['brand'] = brand
	print "result.........",result

        return result

    # Method to get the brands.
    @http.route(
        ['/page/product_brands'],
        type='http',
        auth='public',
        website=True)
    def product_brands(self, **post):
        cr, context, pool = (request.cr,
                             request.context,
                             request.registry)
        b_obj = pool['product.brand']
        domain = []
	print ".............prod brand"
        if post.get('search'):
            domain += [('name', 'ilike', post.get('search'))]
        brand_ids = b_obj.search(cr, SUPERUSER_ID, domain)
        brand_rec = b_obj.browse(cr, SUPERUSER_ID, brand_ids, context=context)

        keep = QueryURL('/page/product_brands', brand_id=[])
        values = {'brand_rec': brand_rec,
                  'keep': keep}
        if post.get('search'):
            values.update({'search': post.get('search')})
        return request.website.render(
            'office_website_product_brand.product_brands',
            values)

    # Method to get the categories.
    @http.route(
        ['/page/product_category'],
        type='http',
        auth='public',
        website=True)
    def product_category(self, **post):
        cr, context, pool = (request.cr,
                             request.context,
                             request.registry)
        c_obj = pool['product.public.category']
        domain = []
        if post.get('search'):
            domain += [('name', 'ilike', post.get('search'))]
        category_ids = c_obj.search(cr, SUPERUSER_ID, domain)
        category_rec = c_obj.browse(cr, SUPERUSER_ID, category_ids, context=context)
        keep = QueryURL('/page/product_category', category_id=[])
        values = {'category_rec': category_rec,
                  'keep': keep}
        if post.get('search'):
            values.update({'search': post.get('search')})
        return request.website.render(
            'office_website_product_brand.product_category',
            values)

