# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class regler_mensualite(osv.osv_memory):
    _name = "wizard.regler.mensualite"
    #_description = "Regle totalité pret "

    _columns = { 
        'pret': fields.many2one('hr.loan','name', required=True, select=True, ondelete='cascade'),
	'montant': fields.char(string="Montant à payer"),
    }

    def reglement_total(self,cr, uid, ids, context=None):
	print "hello u will pay it"
	obj=self.pool.get('hr.loan')
	print "obj===",obj
	id_pret=self.browse(cr,uid,ids,context=context).pret
	print 'pret.......',id_pret
	return True


   
