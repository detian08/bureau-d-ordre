# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime,date

class next_wizard_survey(osv.osv_memory):
    _name = "cci.next.wizard.survey"

    _columns = {
#'product_id':fields.many2one('product.template', 'Produits', required=True),
        #'survey_ids': fields.many2many('survey.survey'),
	'survey_id':fields.many2one('survey.survey', 'Sondage', required=True),
	'question_id':fields.many2one('survey.question', 'Questions', required=True),
	'reponse_id':fields.many2one('survey.label', 'Réponses'),
        'reponse_text':fields.char('Réponses'),
}


    def imprimer(self, cr, uid, ids, context=None):
        datas = {}
        if context is None:
            context = {}
        data = self.read(cr, uid, ids)[0]
        datas = {
            'ids': [],
            'model': 'object.object',
            'form': data,
            'context': 'cci.next.wizard.survey',
        }


	print 'datas.....',datas
        return {'type': 'ir.actions.report.xml', 'report_name': 'jasper_oe_minig_print', 'datas': datas}





    def create_opportunity(self, cr, uid, ids, context):
        datas = {}
        if context:
	    print 'context.....',context
            context = {}
        data = self.read(cr, uid, ids)[0]
        datas = {
            'ids': [],
            'model': 'object.object',
            'form': data
        }


	print 'datas.....',datas

	vals = {
			
			'user_id': uid,
			#'stop':date_deadline,
			'survey_id':context.get('survey'),
			'question_id':context.get('question'),
			'reponse_id':context.get('reponse'),
			'partner_id':1,
       }

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



next_wizard_survey()




