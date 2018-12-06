# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime,date

class fiche_courriel_entrant(osv.osv_memory):
    _name = "cci.wizard.fiche.courriel.entrant"

    _columns = {
        'permanent':fields.boolean('Permanent'),
        'date_debut':fields.date('Date début'),
        'date_fin':fields.date('Date fin'),

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
        return {'type': 'ir.actions.report.xml', 'report_name': 'jasper_fiche_courriel_entrant_print', 'datas': datas}


fiche_courriel_entrant()

