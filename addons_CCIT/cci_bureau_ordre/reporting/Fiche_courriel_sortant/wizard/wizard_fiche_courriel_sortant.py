# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime,date

class fiche_courriel_sortant(osv.osv_memory):
    _name = "cci.wizard.fiche.courriel.sortant"

    _columns = {
        'permanent':fields.boolean('Permanent'),
        'date_debut':fields.date('Date début'),
        'date_fin':fields.date('Date fin'),
	'state' : fields.selection([
        ('draft', "Brouillon"),
        ('to_soumdg', "Soumis à la DG"),
        ('to_soumpre', "Soumis au président"),
 	('to_conseiller', "Soumis au conseiller"),
 	('traite', "Traiter"),
    ], default='draft', string="État"),

    }

    


    def create_report(self, cr, uid, ids, context=None):
        datas = {}
        if context is None:
            context = {}
        data = self.read(cr, uid, ids)[0]
        datas = {
            'ids': [],
            'model': 'object.object',
            'form': data
        }
        return {'type': 'ir.actions.report.xml', 'report_name': 'jasper_fiche_courriel_sortant_print', 'datas': datas}


fiche_courriel_sortant()

