# -*- coding: utf-8 -*-
{
    'name': "CCI PARTENAIRE DISTANCE",
    'description': """
CCI PARTENAIRE.
========================
Ce module gère les partenaires selon un workflow bien déterminé (brouillon, en attente de validation, validé, refusé). De tel sorte, que l'administrateur a le droit de valider l'ajout des partenaires.
""",
    'author': "YAAKOUBI Ghaidaa",
    "website": "http://www.i-way.tn.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Partner',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','mail'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
       # 'views/res_partner_view.xml',
        #'secteur_data.xml',
	    #'views/res_partner_workflow.xml',
	    #'views/res_partner_operateur_view.xml',
	    'views/op_eco_distance.xml',
        'security/ir.model.access.csv',
        #'views/product_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}











# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
