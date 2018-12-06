# -*- coding: utf-8 -*-

{
	"name" : "CCI REPORTING",
	"version" : "0.1",
	"description" : """
CCI REPORTING.
========================
CCI offre la possiblite d'imprimer des rapports spécifiques et de consulter les statistiques concernant les opportunités, les activités, les produits et ses revenus sous forme de tableau de bord """,

	"author" : "Marwa BEN MESSAOUD I-WAY",
	"website" : "http://www.iway-tn.com",

	"depends" : ["base", "jasper_reports",'crm','web_kanban_graph','mail'],
	"category" : "Reporting",
	"init_xml" : ['menuitem.xml',],
	"demo_xml" : [],
	"data_xml" : ['cci_kanban/dashboard_data.xml',
		],
    "update_xml" :[
        	'cci_kanban/dashboard_data.xml',
			'menuitem.xml',
			'cci_kanban/security/ir.model.access.csv',
        	'cci_kanban/crm_dashboard_view.xml',
        	'cci_kanban/crm_dashboard_opportunity.xml',
        	'cci_kanban/crm_dashboard_activity.xml',


			'cci_stat/liste_plaintes/wizard/wizard_liste_plaintes.xml',
			'cci_stat/Etat_revenue/wizard/wizard_etat_revenue.xml',
			'cci_stat/liste_op_eco_non_participant/wizard/wizard_op_eco_non_part.xml',
			'cci_stat/Fiche_product/wizard/wizard_fiche_product.xml',
			'cci_stat/liste_question/wizard/wizard_question_view.xml',
			'cci_stat/liste_opportunity/wizard/wizard_opportunity.xml',
			'cci_stat/Fiche_op_eco/wizard/wizard_fiche_op_eco.xml',
			'cci_stat/Indicateur_performance/wizard/wizard_indicateur_performance.xml',
			'cci_stat/liste_adhesion/wizard/wizard_liste_adhesion.xml',
			'cci_stat/Fiche_activite/wizard/wizard_fiche_activite.xml',
			'cci_stat/oe_secteurs_activite/wizard/wizard_oe_secteurs_activite.xml',
			'cci_stat/Fiche_courriel_sortant/wizard/wizard_fiche_courriel_sortant.xml',
			#'cci_stat/OE_mining/wizard/OE_minig_wizard.xml'



		#'cci_stat/report_options/wizard/wizard_report_options.xml',

		],
	"active": False,
	"installable": True
}

