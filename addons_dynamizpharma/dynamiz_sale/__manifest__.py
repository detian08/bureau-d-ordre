# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sale',
    'version': '1.0',
    'category': 'Human Resources',
    'sequence': 5,
    'description': """Gestion de produit .
=============================================================


""",
    'depends': ['base', 'product','sale','purchase','crm'],
    'data': [
        'views/saleOrder.xml',
    ],
    'demo': [
    ],
    'css': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
