# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2016 Jonathan Bravo, (Guayaquil, Ecuador, http://www.jonathanbravo.com)
#                 Jonathan Bravo <jjbravo88@gmail.com.com>
#
##############################################################################

{
    'name' : 'Profit Dashboard',
    'description': """

Tableau de bord des fatures Clients, fournisseurs et les caisses

	""",
    'version': '8.0.1.0.0',
    'category': 'Accounting',
    'author' : 'Jonathan Bravo @jbravot',
    'complexity': 'normal',
    'website': 'http://jbravot.github.io/portafolio/',
    'data': [
    	'security/dash_security.xml',
        'views/account_journal_dashboard_view.xml',
    ],
    'depends' : [
        'account',
        'web_kanban_graph','share',
    ],
    'js': [],
    'css': [],
    'qweb': [],
    "images": [
		"static/description/example.jpg",
	],
    'installable': True,
    'auto_install': False,
}
