# -*- coding: utf-8 -*-
{
    "name": "CCI PRODUCT",
    "description": """
CCI PRODUCT.
========================
Ce module gère les produits suivant des catégories bien déterminés. 
""",
    "author": "Maroua TURKI & Marwa BEN MESSAOUD I-Way",
    "website": "http://www.i-way.tn.com",
    "category": 'Product',
    "version": '0.1',
    "depends": ['base','hr','sale','crm'],

    # always loaded
    "data": [
	'security/ir.model.access.csv',
        "views/product_view.xml",
        "views/type_product_view.xml",
        "views/type_product_data.xml",
	"views/type_consultation_view.xml",
        "views/type_consultation_data.xml",
        "views/consultation_view.xml",
        "views/reference_consultation.xml",
        #"views/consultation_tags_view.xml",
	"views/product_workflow.xml",
	"views/category_data.xml",
	"views/category_view.xml",
	"wizard/wizard.xml",
	"wizard/contact_wizard_view.xml",
    ],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo.xml',
   #],
}


