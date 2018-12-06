{
	'name' : 'Gestion des prets',
	'version' : '0.1',
	'author' : 'Marwa ROMDHAN',
	'category' : 'Human Resources',
	'description' : """Gestion des demandes des prets :
		les prets societe 
		Paiement mensuel des tranches du prets

	""",

	'depends' : [ 'hr_contract'],#'hr_payroll'
	'data': [
	    'security/ir.model.access.csv',
	    'security/ir_rule.xml',
		'sequences/hr_loan_sequence.xml',
		'views/hr_loan_view.xml',
        #'wizards/regler_mensualite.xml',
	],

	'installable': True,
	'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
