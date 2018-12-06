# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime,date

class next_wizard_opportunity(osv.osv_memory):
    _name = "cci.next.wizard.opportunity"

    _columns = {
        'product_id':fields.many2one('product.template', 'Produits'),
}


    def imprimer(self, cr, uid, ids, context=None):
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
        return {'type': 'ir.actions.report.xml', 'report_name': 'jasper_oe_minig_print', 'datas': datas}




    def create_opportunity(self, cr, uid, ids,context):
       # datas = {}
       # if context is None:
            #context = {}
	    
###########################condition=survey#################################

	    if context:
	    	print 'context.....',context

		active_model = context.get('active_model')
		if active_model == 'cci.next.wizard.survey':
			survey_id = context.get('survey')
			question_id = context.get('question')
			reponse_id = context.get('reponse')
			if reponse_id :
			    	survey_user_input = self.pool.get('survey.user_input').search(cr, uid, [('survey_id','=',survey_id)])


			    	for user_input in survey_user_input:
			    		input_lines = self.pool.get('survey.user_input_line').search(cr, uid, [('question_id','=',question_id), ('user_input_id','=',user_input),('value_suggested','=',reponse_id)])
				    	for input_line in input_lines:
						input_id = self.pool.get('survey.user_input_line').browse(cr,uid,input_line).user_input_id.id
						partner_id=self.pool.get('survey.user_input').browse(cr,uid,input_id).partner_id.id
						vals = {
			
								'user_id': uid,
								'type':'opportunity',
								'product_id':context.get('product'),
								'partner_id':partner_id,

					       }
						create_id = self.pool.get('crm.lead').create(cr, uid, vals, context=context)
						return create_id


######condition=consultation#############



		if active_model == 'cci.next.wizard.consultation':
			tags_ids = context.get('tags')
			print tags_ids
			for tag_id in tags_ids[0][2]:
				print tag_id
				cr.execute("SELECT consult_id FROM consult_tag_rel WHERE tag_id =%s",(tag_id,))
				#cr.execute("SELECT consult_id FROM consult_tag_rel WHERE (tag_id =%s",(tuple(tag_id),))
				lines = cr.dictfetchall()
				for line in lines :
					consult_id= line['consult_id']
					print 'consult_id',consult_id
		            		op_eco_id=self.pool.get('cci.consultation').browse(cr,uid,consult_id).op_eco_id
		            		print 'op_eco_id: ',op_eco_id

		#data = self.read(cr, uid, ids)[0]
			#partner_id = self.pool.get('res.partner').browse(cr,uid,context=context).id
					vals = {
				
							'user_id': uid,
							'type':'opportunity',
							'product_id':context.get('product'),
							'partner_id':op_eco_id,
				       }
					print 'vals:',vals
					create_id = self.pool.get('crm.lead').create(cr, uid, vals, context=context)
				    	print 'create_id.....',create_id
					return create_id
#########survey##############


    def retour_wizard(self, cr, uid, ids, context):
        datas = {}
        if context:
		active_model = context.get('active_model')
		if active_model == 'cci.next.wizard.consultation':
			return {
			'name': ('OE Mining'),
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'cci.next.wizard.consultation',
			'view_id ref= consultation_template_form_view':True,

			'type': 'ir.actions.act_window',
			'target': 'new',

		}
		if active_model == 'cci.next.wizard.survey':

			return {
			'name': ('OE Mining'),
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'cci.next.wizard.survey',
			'view_id ref= survey_form_inherit':True,

			'type': 'ir.actions.act_window',
			'target': 'new',

		}



next_wizard_opportunity()




