# -*- coding: utf-8 -*-
{
    "name": "CCI Bureau d'ordre",
    "description": """
CCI BUREAU D'ORDRE
========================
Ce module gère les courriels entrants et sortants d'un bureau d'ordre. 
""",
    "author": "Yaakoubi Ghaidaa I-Way",
    "website": "http://www.i-way.tn.com",
    "category": 'Courriels',
    "version": '0.1',
    "depends": ['base','hr','sale','crm'],

    # always loaded
    "data": [


        "views/courriel.xml",
        "views/reference_courriel_sortant.xml",
        "views/reference_courriel_entrant.xml",
	"views/courriel_entrant_view.xml",
	"views/courriel_sortant_view.xml",
	"views/to_do_entrant.xml",
	"views/to_do_sortant.xml",


	"views/cci_courriel_entrant_workflow.xml",
	"views/cci_courriel_sortant_workflow.xml",
        "views/importance.xml",
        "views/urgence.xml",
        "views/note.xml",
        "views/instruction.xml",
        "views/type.xml",
        "views/mode_reception_view.xml",
        "views/degre.xml",
	'reporting/Fiche_courriel_entrant/wizard/wizard_fiche_courriel_entrant.xml',
	'reporting/Fiche_courriel_sortant/wizard/wizard_fiche_courriel_sortant.xml',
	'wizard/delegue_pouvoir/wizard/wizard_delegue_pouvoir.xml',
	'wizard/annuler_pouvoir/wizard/wizard_annuler_pouvoir.xml',





    	'security/cci_security.xml',
        'security/ir.model.access.csv',
    	'security/cci_record_rules.xml',



	#"wizard/wizard_fiche_courriel_sortant.xml",
        
        #"views/reference_consultation.xml",
        #"views/consultation_tags_view.xml",
	#"views/product_workflow.xml",
	#"views/category_data.xml",
	#"views/category_view.xml",
	#"wizard/wizard.xml",
	#"wizard/contact_wizard_view.xml",
    ],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo.xml',
   #],
}


