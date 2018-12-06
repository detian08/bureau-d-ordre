# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime,date


class next_wizard_consultation(osv.osv_memory):
    _name = "cci.next.wizard.consultation"

    _columns = {
        'tags_ids': fields.many2many('cci.consultation.tags', 'cci_wizard_tags_rel', 'wizard_id','tag_id'),
	#'tags_id': fields.text('Tags'),
}


    def imprimer(self, cr, uid, ids, context=None):
        print 'imprimer consultation..............'
        datas = {}

        if context is None:
            context = {}
        data = self.read(cr, uid, ids)[0]

        datas = {
            'ids': [],
            'model': 'object.object',
            'form': data,
            'context':'cci.next.wizard.consultation',


        }
        return {'type': 'ir.actions.report.xml', 'report_name': 'jasper_oe_minig_print', 'datas': datas}




    def create_opportunity(self, cr, uid, ids, context):
		#tags_ids = self.browse(cr,uid,ids,context).tags_ids
		#for tag_id in tags_ids:
		#	context=({'tags_ids','=',tag_id.id})
		#print context
		return {
		'name': ('Opportunité'),
		'view_type': 'form',
		'view_mode': 'form',
		'res_model': 'cci.next.wizard.opportunity',
		'view_id ref= cci_crm_form_view':True,
		'type': 'ir.actions.act_window',
		'target': 'new',

	}

    def retour_wizard_oe_minig(self, cr, uid, ids, context=None):
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



	return {
	'name': ('OE Mining'),
	'view_type': 'form',
	'view_mode': 'form',
	'res_model': 'cci.wizard.oe.mining',
	'view_id ref= wizard_mining_view':True,

	'type': 'ir.actions.act_window',
	'target': 'new',

}



next_wizard_consultation()

