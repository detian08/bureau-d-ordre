# -*- coding: utf-8 -*-
from openerp import http
import base64
from openerp import SUPERUSER_ID
from openerp import models, fields, api
from openerp.http import request

from openerp.addons.website.models.website import slug

class example(http.Controller):
    #@http.route('/page/example/detail', auth='public')
    #def example(self, **kw):
	#print ".............................."
	#companies = http.request.env['res.company'].search([])
	#print "..............................",companies
	#companies = http.request.env['res.company'].sudo().search([])
	#vals = {'companies': companies}
	#return http.request.render()

	  # pass company details to the webpage in a variable
       # return "Hello, world"
#exple à suivre
    @http.route('/page/stages', auth='public', website=True)    
    def example(self, **kw):
        #return "Hello World"        
	companies = http.request.env['iway_pfe.iway_pfe'].search([])      
  	return http.request.render('iway_test_web.index', { 'companies': companies})

class Academy(http.Controller):
    @http.route('/academy/academy/', auth='public')
    def index(self, **kw):
        return http.request.render('iway_test_web.index', {
            'teachers': ["Diana Padilla", "Jody Caroll", "Lester Vaughn"],
        })

#id stage  
#template detail (bouton apply)
    @http.route('/page/stages/detail/<model("iway.pfe"):company>', type='http', auth="public", website=True)
    def stages_detail(self, company, **kwargs):
	print "................",company
        return request.render("iway_test_web.detail", {
            'stage': stage,
            'main_object': stage,
        })
#template apply (formulaire à remplir )
    @http.route('/page/stages/apply/<model("iway_pfe.iway_pfe"):stage>', type='http', auth="public", website=True)
    def stages_apply(self, stage):
		print '..........................',stage
		error = {}
		default = {}
		if 'iway_test_web_error' in request.session:
		    error = request.session.pop('iway_test_web_error')
		    default = request.session.pop('iway_test_web_default')

		return request.render("iway_test_web.apply", {
		    'stage': stage,
		    'error': error,
		    'default': default,
		})

#id stage
	 
    #@http.route('/page/example', type='http', auth='public', website=True)
    #def render_example_page(self):
#	print "........................................."
#        return http.request.render('create_webpage_demo.example', {})
    #@http.route('/page/example/detail', type='http', auth='public', website=True)
    def navigate_to_detail_page(self):
	print ".................detail........................"
        #return http.request.render('create_webpage_demo.example', {})
	companies = self.env['res.company'].search([])
	companies = http.request.env['res.company'].sudo().search([])
	return http.request.render({
	  # pass company details to the webpage in a variable
	  'companies': companies})

    #@http.route('/page/example/detail', type='http', auth='public', website=True)
    #def navigate_to_detail_page(self):
        # This will get all company details (in case of multicompany this are multiple records)
     #   companies = http.request.env['res.company'].sudo().search([])
       # return http.request.render('create_webpage_demo.example', {
          # pass company details to the webpage in a variable
      #    'companies': companies})


class Academy(http.Controller):
    @http.route('/academy/academy/', auth='public')
    def index(self, **kw):
        return "Hello, world"

