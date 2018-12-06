# -*- coding: utf-8 -*-

{
    'name': 'SPS Payment Acquirer',
    'category': 'Hidden',
    'summary': 'Payment Acquirer: SPS Implementation',
    'version': '1.0',
    'description': """SPS Payment Acquirer""",
    'author': 'Marwa BEN MESSAOUD I-WAY',
    'depends': ['payment'],
    'data': [
        'sps.xml',
        'payment_acquirer.xml',
        'res_config_view.xml',
        'sps.xml',
    ],
    'installable': True,
}
