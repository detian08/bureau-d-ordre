# -*- coding: utf-8 -*-

{
    'name': 'Product Brand / Category Filtering in Website',
    'category': 'e-commerce',
    'author': "Serpent Consulting Services Pvt. Ltd,"
              "Odoo Community Association (OCA),"
	      "Marwa BEN MESSAOUD I-WAY",
    'website': "http://www.serpentcs.com, ""http://www.iway-tn.com",
    'version': '8.0.1.0.0',
    'depends': [
        'office_product_brand',
        'website_sale'
    ],
    'data': [
        "security/ir.model.access.csv",
        "views/product_brand.xml",
	"views/product_categories.xml",
    ],
    'installable': True,
    'auto_install': False,
}
