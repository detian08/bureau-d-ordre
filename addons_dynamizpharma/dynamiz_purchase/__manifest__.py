# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Purchases',
    'version': '1.0',
    'category': 'Human Resources',
    'sequence': 5,
    'description': """Gestion de produit .
=============================================================


""",
    'depends': ['base', 'product','sale','purchase'],
    'data': [
        'views/purchases.xml',
    ],
    'demo': [
    ],
    'css': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
