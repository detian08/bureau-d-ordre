# -*- coding: utf-8 -*-
{
    "name": "CCI Users",
    "description": """
CCI PRODUCT.
========================
Ce module gère les produits suivant des catégories bien déterminés. 
""",
    "author": "YAAKOUBI Ghaida I-Way",
    "website": "http://www.i-way.tn.com",
    "category": 'Product',
    "version": '0.1',
    "depends": ['base','hr','sale','crm'],

    # always loaded
    "data": [
	#'security/ir.model.access.csv',
        #"views/product_view.xml",
        #"views/type_product_view.xml",
        #"views/type_product_data.xml",
	#"views/type_consultation_view.xml",
         "views/cci_res_users.xml",
 
    ],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo.xml',
   #],
}


