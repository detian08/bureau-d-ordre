# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime,date

class fiche_oe_sect_act(osv.osv_memory):
    _name = "cci.wizard.fiche.oe.sect.act"

    _columns = {
        'sect_act_ids': fields.many2many('res.partner.category','secteur_operateur_rel', required=True),
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
	print 'datas.....',datas
        return {'type': 'ir.actions.report.xml', 'report_name': 'jasper_oe_secteurs_activite_print', 'datas': datas}


fiche_oe_sect_act()

