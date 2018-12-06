# coding: utf-8
import json
import logging
import werkzeug
import werkzeug.utils
from datetime import datetime
from math import ceil

from openerp import SUPERUSER_ID
from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT as DTF, ustr
from openerp.addons.survey.controllers.main import WebsiteSurvey

class WebsiteSurvey_inherit(WebsiteSurvey):

    # Survey displaying
    @http.route(['/survey/fill/<model("survey.survey"):survey>/<string:token>',
                 '/survey/fill/<model("survey.survey"):survey>/<string:token>/<string:prev>'],
                type='http', auth='public', website=True)
    def fill_survey(self, survey, token, prev=None, **post):
        '''Display and validates a survey'''
        cr, uid, context = request.cr, request.uid, request.context
        survey_obj = request.registry['survey.survey']
        partner_obj = request.registry['res.partner']
        user_input_obj = request.registry['survey.user_input']
        user_input_line_obj = request.registry['survey.user_input_line']
        surveu_page_obj = request.registry['survey.page']
        surveu_question_obj = request.registry['survey.question']

        # Controls if the survey can be displayed
        errpage = self._check_bad_cases(cr, uid, request, survey_obj, survey, user_input_obj, context=context)
        if errpage:
            return errpage

        # Load the user_input
        try:
            user_input_id = user_input_obj.search(cr, SUPERUSER_ID, [('token', '=', token)])[0]
        except IndexError:  # Invalid token
            return request.website.render("website.403")
        else:
            user_input = user_input_obj.browse(cr, SUPERUSER_ID, [user_input_id], context=context)[0]

        # Do not display expired survey (even if some pages have already been
        # displayed -- There's a time for everything!)
        errpage = self._check_deadline(cr, uid, user_input, context=context)
        if errpage:
            return errpage
        # Select the right page
        if user_input.state == 'new':  # First page
            page, page_nr, last = survey_obj.next_page(cr, uid, user_input, 0, go_back=False, context=context)
            data = {'survey': survey, 'page': page, 'page_nr': page_nr, 'token': user_input.token}
            if last:
                data.update({'last': True})
            return request.website.render('survey.survey', data)

        elif user_input.state == 'done':  # Display success message
            partner_id = user_input_obj.browse(cr, SUPERUSER_ID, user_input.id, context=context).partner_id
            if not partner_id:
                survey_id = user_input_obj.browse(cr, SUPERUSER_ID, user_input.id, context=context).survey_id.id
                #question_id = surveu_question_obj.browse(cr, SUPERUSER_ID, user_input.id, context=context).question_id.id
                page_ids = surveu_page_obj.search(cr, SUPERUSER_ID,[('survey_id', '=', survey_id)])
                for page_id in page_ids:
                    ###get question_id
                    #question_id_name = surveu_question_obj.search(cr, SUPERUSER_ID,[('page_id', '=', page_id), ('question', '=', u'Nom opérateur économique')])
	            #print 'question_id_name.....',question_id_name
                    question_id_denomination_entreprise = surveu_question_obj.search(cr, SUPERUSER_ID,[('page_id', '=', page_id), ('question', '=', u"quelle est la dénomination de l'entreprise ?")])
	            print 'question_id_denomination_entreprise.....',question_id_denomination_entreprise
                    #question_id_tel = surveu_question_obj.search(cr, SUPERUSER_ID, [('page_id', '=', page_id), ('question', '=', u'Numéro de téléphone')])
                    #question_id_mail = surveu_question_obj.search(cr, SUPERUSER_ID, [('page_id', '=', page_id), ('question', '=', u'E-mail')])
                    #question_id_mf = surveu_question_obj.search(cr, SUPERUSER_ID, [('page_id', '=', page_id), ('question', '=', u'Matricule Fiscal')])
                    ###get answer_id
                    answer_denomination_entreprise_id = user_input_line_obj.search(cr, SUPERUSER_ID, [('question_id', '=', question_id_denomination_entreprise),('user_input_id', '=', user_input.id),('survey_id', '=', survey_id)])
	            print 'answer_denomination_entreprise_id.....',answer_denomination_entreprise_id
                    #answer_name_id = user_input_line_obj.search(cr, SUPERUSER_ID, [('question_id', '=', question_id_name),('user_input_id', '=', user_input.id),('survey_id', '=', survey_id)])
	            #print 'answer_name_id.....',answer_name_id
                    #answer_tel_id = user_input_line_obj.search(cr, SUPERUSER_ID, [('question_id', '=', question_id_tel),('user_input_id', '=', user_input.id),('survey_id', '=', survey_id)])
                    #answer_mail_id = user_input_line_obj.search(cr, SUPERUSER_ID, [('question_id', '=', question_id_mail),('user_input_id', '=', user_input.id),('survey_id', '=', survey_id)])
                    #answer_mf_id = user_input_line_obj.search(cr, SUPERUSER_ID, [('question_id', '=', question_id_mf),('user_input_id', '=', user_input.id),('survey_id', '=', survey_id)])
                    ###get answer
                    answer_denomination_entreprise = user_input_line_obj.browse(cr, SUPERUSER_ID, answer_denomination_entreprise_id,context=context).value_text
	            print 'answer_denomination_entreprise.....',answer_denomination_entreprise
                    #answer_name = user_input_line_obj.browse(cr, SUPERUSER_ID, answer_name_id,context=context).value_text
	            #print 'answer_name.....',answer_name
                    #answer_mail = user_input_line_obj.browse(cr, SUPERUSER_ID, answer_mail_id,context=context).value_text
                    #answer_mf = user_input_line_obj.browse(cr, SUPERUSER_ID, answer_mf_id,context=context).value_text
                    #answer_tel = user_input_line_obj.browse(cr, SUPERUSER_ID, answer_tel_id, context=context).value_text
                    ###get partner_id
####appel
		    vals = {
		    #'name':answer_name,
		    #'vat':answer_mf,
		    #'email':answer_mail,
		    #'mobile':answer_tel,
		    'name':answer_denomination_entreprise,

		    }
	            print 'vals.....',vals
		    partner_id = partner_obj.search_partner(cr,uid,vals,context=None)
	            print 'partner_id.....',partner_id

                    if partner_id:
                        user_input_obj.write(cr, SUPERUSER_ID, user_input.id, {'partner_id':partner_id[0]},context=context)
            return request.website.render('survey.sfinished', {'survey': survey,'token': token,'user_input': user_input})
        elif user_input.state == 'skip':
            flag = (True if prev and prev == 'prev' else False)
            page, page_nr, last = survey_obj.next_page(cr, uid, user_input, user_input.last_displayed_page_id.id, go_back=flag, context=context)

            #special case if you click "previous" from the last page, then leave the survey, then reopen it from the URL, avoid crash
            if not page:
                page, page_nr, last = survey_obj.next_page(cr, uid, user_input, user_input.last_displayed_page_id.id, go_back=True, context=context)

            data = {'survey': survey, 'page': page, 'page_nr': page_nr, 'token': user_input.token}
            if last:
                data.update({'last': True})
            return request.website.render('survey.survey', data)
        else:
            return request.website.render("website.403")

