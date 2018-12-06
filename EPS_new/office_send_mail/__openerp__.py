# -*- coding: utf-8 -*-

{
        "name" : "Office Send Mail",
        "version" : "0.1",
        "author" : "Houssem Abid & Maroua TURKI & Marwa BEN MESSAOUD",
        "website" : "http://iway-tn.com/",
        "category" : "Sale",
        "description": """Module pour l'envoie des devis de vente""",
        "depends" : ['base','office_sale_devis',],
        "init_xml" : [ ],
        "test" : ['tests/tests.yml'],
        "demo_xml" : [ ],
        "update_xml" : ['views/sale_devis_view.xml','views/mail_wiz_workflow.xml'],
        "installable": True,

}
