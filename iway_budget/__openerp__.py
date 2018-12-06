# -*- coding: utf-8 -*-
{
    'name': "iway_budget",

    'author': "Amal CHAABEN I-WAY",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
        #'views/reference.xml',
        #'views/reference_num_ordre.xml',
        'views/budget_line_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
