# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime

class wizard_fiche_client(osv.osv_memory):
    _name = "wizard.fiche.fournisseur"
    _description = "Fiche Fournisseur Wizard "

    _columns = {
        'partner_id':fields.many2one('res.partner', 'Fournisseur', required=True),
        'date1': fields.date(required=True),
        'date2': fields.date(required=True),
    }

    def _check_period(self, cr, uid, ids, context=None):
        for val in self.read(cr, uid, ids, ['date1', 'date2'], context=context):
            if val['date2'] < val['date1']:
                return False
        return True

    _constraints = [
        (_check_period, u'Erreur: La deuxième date doit être supèrieure à la première', ['date2'])
    ]



    def create_report(self, cr, uid, ids, context=None):
	print 'heloo fiche fournisseur wizard..........'
        datas = {}
        if context is None:
            context = {}
        data = self.read(cr, uid, ids)[0]
        datas = {
            'ids': [],
            'model': 'object.object',
            'form': data
        }
        return {'type': 'ir.actions.report.xml', 'report_name': 'jasper_fiche_fournisseur_print', 'datas': datas}


wizard_fiche_client()
