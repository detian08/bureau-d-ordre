# -*- coding: utf-8 -*-
{
    'name': "iway_Stage",

    'summary': """
       """,

    'description': """
       
    """,

    'author': "Ghaida YAAKOUBI",
    'website': "http://www.iway-tn.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'PFE',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','hr_recruitment'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
	'iway_stage_workflow.xml',
        'iway_stage.xml',
        'iway_stage_pfa_workflow.xml',
	'iway_stage_ste_workflow.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
