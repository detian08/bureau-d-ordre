# -*- coding: utf-8 -*-
from openerp import http

# class BulletinSoin(http.Controller):
#     @http.route('/bulletin_soin/bulletin_soin/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bulletin_soin/bulletin_soin/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bulletin_soin.listing', {
#             'root': '/bulletin_soin/bulletin_soin',
#             'objects': http.request.env['bulletin_soin.bulletin_soin'].search([]),
#         })

#     @http.route('/bulletin_soin/bulletin_soin/objects/<model("bulletin_soin.bulletin_soin"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bulletin_soin.object', {
#             'object': obj
#         })