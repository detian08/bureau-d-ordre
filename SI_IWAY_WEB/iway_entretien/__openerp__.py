# -*- coding: utf-8 -*-
{
    'name': "iway_entretien",

    'summary': """
       """,

    'description': """
       
    """,

    'author': "Ghaida YAAKOUBI",
    'website': "http://www.iway-tn.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'ENTRETIEN',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
	'iway_entretien-worflow.xml',
        'iway_entretien.xml',
        'entretien_evaluation.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
