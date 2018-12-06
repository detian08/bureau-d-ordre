# -*- coding: utf-8 -*-
{
    'name': "CCI PARTENAIRE DISTANCE",
    'description': """
CCI PARTENAIRE DISTANCE.
========================
Ce module permet de calculer la distance entre les partenaires qui sont en attentes de validation et les opérateurs économiques existants à travers l'algorithme de jaro
""",
    'author': "YAAKOUBI Ghaidaa",
    "website": "http://www.i-way.tn.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Partner',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
	    #'views/res_partner_distance_views.xml',
	    'views/res_partner_request_distance_views.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}











# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
