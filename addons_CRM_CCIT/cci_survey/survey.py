# -*- coding: utf-8 -*-
from openerp import api
from openerp.tools.translate import _
from openerp.osv import fields, osv
from openerp.exceptions import Warning

class survey_survey(osv.Model):
    _name = 'survey.survey'
    _inherit ='survey.survey'

    _columns = {
	'product_id' :fields.many2one('product.template', string="Produit", required=True),
    }

    def create(self, cr, uid, vals, context=None):
        cr.execute('SELECT id FROM survey_survey')
        res = cr.fetchall()
        survey_ids = [x[0] for x in res]

        survey_id = max(survey_ids)

        # survey_id = super(survey_survey, self).create(cr, uid, vals, context=context)

        vals_page = {
            'survey_id':survey_id,
            'title':"SECTION A: IDENTIFICATION DE L'ENREPRISE",
        }
        page_id = self.pool.get('survey.page').create(cr,uid,vals_page,context=context)


        vals_question_one ={
            'page_id':page_id,
            'question':"quelle est la fonction du répondant ?",
            'type':'simple_choice',
        }
	question_one_id = self.pool.get('survey.question').create(cr, uid, vals_question_one, context=context)

################## la fonction de répondant ###########""""



	vals_label_one = {
	'question_id': question_one_id,
	'value': 'Diretceur',

	}


	label_one_id = self.pool.get('survey.label').create(cr, uid, vals_label_one, context=context)

	vals_label_two = {
	    'question_id': question_one_id,
	    'value': 'Responsable',

	}


	label_two_id = self.pool.get('survey.label').create(cr, uid, vals_label_two, context=context)

	vals_label_three = {
	'question_id': question_one_id,
	'value': 'Employé',

	}


	label_three_id = self.pool.get('survey.label').create(cr, uid, vals_label_three, context=context)


	vals_label_four = {
	'question_id': question_one_id,
	'value': 'Employé',

	}


	label_four_id = self.pool.get('survey.label').create(cr, uid, vals_label_four, context=context)

	##################################### Contact du répondant ###################################
	#question_one_id = self.pool.get('survey.question').create(cr, uid, vals_question_one, context=context)


	vals_question_two ={
	    'page_id':page_id,
	    'question':"Quel est le nom  du répondant ?",
	    'type':'textbox',
	}
	question_two_id = self.pool.get('survey.question').create(cr, uid, vals_question_two, context=context)




	vals_question_three ={
	    'page_id':page_id,
	    'question':"Quel est le Numéro de téléphone du répondant ?",
	    'type':'textbox',
	}
	question_three_id = self.pool.get('survey.question').create(cr, uid, vals_question_three, context=context)

	vals_question_four = {
	    'page_id': page_id,
	    'question': "Quelle est l'adresse du répondant ?",
	    'type': 'textbox',
	}
	question_four_id = self.pool.get('survey.question').create(cr, uid, vals_question_four, context=context)


	vals_question_five = {
	    'page_id': page_id,
	    'question': 'Quel est le Email du répondant ?',
	    'type': 'textbox',
	}
	question_five_id = self.pool.get('survey.question').create(cr, uid, vals_question_five, context=context)
	#########################################"dénomination de l'entreprise#################



	vals_question_denomination ={
	    'page_id':page_id,
	    'question':"quelle est la dénomination de l'entreprise ?",
	    'type':'textbox',
	}
	question_denomination_id = self.pool.get('survey.question').create(cr, uid, vals_question_denomination, context=context)
	##################secteur d'activité###########""""

	vals_question_secteur ={
	    'page_id':page_id,
	    'question':"Quels sont les secteurs d'activité ?",
	    'type':'multiple_choice',
	}
	question_secteur_id = self.pool.get('survey.question').create(cr, uid, vals_question_secteur, context=context)




	vals_label_secteur_one = {
	'question_id': question_secteur_id,
	'value': 'Commerce',

	}


	label_secteur_one_id = self.pool.get('survey.label').create(cr, uid, vals_label_secteur_one, context=context)

	vals_label_secteur_two = {
	    'question_id': question_secteur_id,
	    'value': 'Industrie,mines,BTP',

	}


	label_secteur_two_id = self.pool.get('survey.label').create(cr, uid, vals_label_secteur_two, context=context)

	vals_label_secteur_three = {
	'question_id': question_secteur_id,
	'value': 'Services',

	}


	label_secteur_three_id = self.pool.get('survey.label').create(cr, uid, vals_label_secteur_three, context=context)


	vals_secteur_label_four = {
	'question_id': question_secteur_id,
	'value': 'Agriculture',

	}


	label_secteur_four_id = self.pool.get('survey.label').create(cr, uid, vals_secteur_label_four, context=context)

	###################################artisan ou nn#####################################




	vals_question_artisan ={
	    'page_id':page_id,
	    'question':'Êtes-vous artisan ?',
	    'type':'simple_choice',
	}
	question_artisan_id = self.pool.get('survey.question').create(cr, uid, vals_question_artisan, context=context)



	vals_label_artisan_one = {
	'question_id': question_artisan_id,
	'value': 'Oui',

	}


	label_artisan_one_id = self.pool.get('survey.label').create(cr, uid, vals_label_artisan_one, context=context)




	vals_label_artisan_two = {
	'question_id': question_artisan_id,
	'value': 'Non',

	}


	label_artisan_two_id = self.pool.get('survey.label').create(cr, uid, vals_label_artisan_two, context=context)


	vals_label_artisan_three = {
	'question_id': question_artisan_id,
	'value': 'Ne se prononce pas',

	}


	label_artisan_three_id = self.pool.get('survey.label').create(cr, uid, vals_label_artisan_three, context=context)

	#######################activité principale de l'entreprise##################

	vals_question_activite ={
	    'page_id':page_id,
	    'question':"Quelle est l'activité principale de l'entreprise ?",
	    'type':'textbox',
	}
	question_activite_id = self.pool.get('survey.question').create(cr, uid, vals_question_activite, context=context)
##################effectif salariés permanents#############



	vals_question_effectif ={
	'page_id':page_id,
	'question':"Quelle est l'effectif salariés permanents ?",
	'type':'simple_choice',
	}
	question_effectif_id = self.pool.get('survey.question').create(cr, uid, vals_question_effectif, context=context)

		

	vals_label_effectif_one ={
	'question_id': question_effectif_id,
	'value': '0 Salarié',

	}


	label_effectif_one_id = self.pool.get('survey.label').create(cr, uid, vals_label_effectif_one, context=context)




	vals_label_effectif_two ={
	'question_id': question_effectif_id,
	'value': '1 à 9 Salariés',

	}


	label_artisan_two_id = self.pool.get('survey.label').create(cr, uid, vals_label_effectif_two, context=context)


	vals_label_effectif_three ={
	'question_id': question_effectif_id,
	'value': '10 à 49 salariés',

	}


	label_effectif_three_id = self.pool.get('survey.label').create(cr, uid, vals_label_effectif_three, context=context)

	vals_label_effectif_four ={
	 'question_id': question_effectif_id,
	 'value': '50 à 250 salariés',

	}


	label_effectif_four_id = self.pool.get('survey.label').create(cr, uid, vals_label_effectif_four, context=context)
	print '................................'
	vals_label_effectif_five ={
	'question_id': question_effectif_id,
	'value': 'plus de 250 salariés',

	}


	label_effectif_five_id = self.pool.get('survey.label').create(cr, uid, vals_label_effectif_five, context=context)
	############################"ancienneté de l'entreprise ###############"



	vals_question_anciennete ={
	    'page_id':page_id,
	    'question':"Quelle est l'ancienneté de l'entreprise ?",
	    'type':'simple_choice',
	}
	question_anciennete_id = self.pool.get('survey.question').create(cr, uid, vals_question_anciennete, context=context)



	vals_label_anciennete_one ={
	'question_id': question_anciennete_id,
	'value': 'Moins de 1 an',

	}


	label_anciennete_one_id = self.pool.get('survey.label').create(cr, uid, vals_label_anciennete_one, context=context)




	vals_label_anciennete_two ={
	'question_id': question_anciennete_id,
	'value': 'Entre 1 et 5 ans',

	}


	label_artisan_two_id = self.pool.get('survey.label').create(cr, uid, vals_label_anciennete_two, context=context)


	vals_label_anciennete_three ={
	'question_id': question_anciennete_id,
	'value': 'Plus de 5 ans',

	}


	label_anciennete_three_id = self.pool.get('survey.label').create(cr, uid, vals_label_anciennete_three, context=context)

	#########################""chiffre d'affaires hors taxes en 2017 ######################"

	vals_question_chiffre ={
	'page_id':page_id,
	'question':"Quel est le chiffre d'affaires hors taxes en 2017?",
	'type':'simple_choice',
	}
	question_chiffre_id = self.pool.get('survey.question').create(cr, uid, vals_question_chiffre, context=context)



	vals_label_chiffre_one ={
	'question_id': question_chiffre_id,
	'value': 'pas de CA en 2017',

	}


	label_chiffre_one_id = self.pool.get('survey.label').create(cr, uid, vals_label_chiffre_one, context=context)




	vals_label_chiffre_two ={
	'question_id': question_chiffre_id,
	'value': 'Moins de 5 millions FCFA',

	}


	label_artisan_two_id = self.pool.get('survey.label').create(cr, uid, vals_label_chiffre_two, context=context)


	vals_label_chiffre_three ={
	'question_id': question_chiffre_id,
	'value': 'Entre 5 et 50 millions FCFA',

	}


	label_chiffre_three_id = self.pool.get('survey.label').create(cr, uid, vals_label_chiffre_three, context=context)



	vals_label_chiffre_four ={
	'question_id': question_chiffre_id,
	'value': 'Entre 50 et 200 millions FCFA',

	}


	label_chiffre_four_id = self.pool.get('survey.label').create(cr, uid, vals_label_chiffre_four, context=context)

	vals_label_chiffre_five ={
	'question_id': question_chiffre_id,
	'value': 'Plus de 200 millions FCFA',

	}


	label_chiffre_five_id = self.pool.get('survey.label').create(cr, uid, vals_label_chiffre_five, context=context)
######################"
	survey_id = super(survey_survey, self).create(cr, uid, vals, context=context)
	page_id = self.pool.get('survey.page').write(cr, uid, page_id, {'survey_id':survey_id}, context=context)

	return survey_id

class survey_mail_compose_message(osv.TransientModel):
    _inherit = 'survey.mail.compose.message'
    _columns = {
        'public': fields.selection([('email_public_link', 'Send by email the public web link to your audience.'),],string='Share options', required=True),
        'filter_type': fields.selection(
            [('product', u'Tous les opérateurs économiques qui ont commandé un produit particulier'),
             ('etat_adhesion', u'Tous les opérateurs économiques qui ont une adhésion'),
             ('secteur_activite',u'Tous les opérateurs économiques qui appartient à un ou plusieurs secteurs d\'activités'),
             ('group', u'Tous les opérateurs économiques qui appartient à un groupe particulier')], string="Critère"),

        'product_id': fields.many2one('product.template', 'Produit'),
        'etat_adhesion': fields.selection([('membre_payant', u'Membre payant'), ('autre', 'Autre')],u'Etat d\'adhésion'),
        'secteur_activite': fields.many2many('res.partner.category', 'mail_info_filtre_categ_res_partner_rel','categ_res_partner_id', 'mail_info_filtre_id', u'Secteur d\'activité'),
        'group_id': fields.many2one('res.partner.group', 'Groupe particulier'),
        'recipient_ids': fields.many2many('res.partner', string='À (Partenaires)'),
    }

    @api.onchange('product_id')
    def onchange_case_product_id(self):
        res = {}
        prod_ids = []
        lead_ids = self.env['crm.lead'].sudo().search([('stage_id', '=', 6)])
        for obj in lead_ids:
            id_prod = obj.product_id.id
            prod_ids.append(id_prod)
        res['domain'] = {'product_id': [('id', 'in', prod_ids)]}
        return res

    @api.onchange('recipient_ids')
    def on_change_recipient_ids(self):
        list_mail=[]
        list_partner=[]
        print '..recipient_ids..',self.recipient_ids
        for recipient_id in self.recipient_ids:
            print '...recipient_id...',recipient_id

            self.multi_email = ''
            print '1 self.multi_email',self.multi_email
            partner_id = recipient_id.id
            email_partner = self.env['res.partner'].browse(partner_id).email
            print 'email_partner', email_partner

            if email_partner != False:
                list_mail.append(str(email_partner) + ',')
                # self.multi_email = str(list_mail).strip('[]').strip("''").strip("', '")
                # print 'Les emails :', self.multi_email

                list_partner.append(partner_id)
                print 'list_partner', list_partner
                self.recipient_ids = [(6, 0, list_partner)]



    @api.onchange('product_id', 'etat_adhesion','secteur_activite','group_id')
    def on_change_mail(self):
        list_partner=[]
        list_mail = []
        self.recipient_ids = [(6, 0, [])]
        self.multi_email = ''
        print '1 self.multi_email', self.multi_email
        if self.filter_type == 'product':

            if self.product_id:
                print 'if .....'
                lead_ids = self.env['crm.lead'].search([('stage_id', '=', 6),('product_id', '=', self.product_id.id)])
            else:
                lead_ids = self.env['crm.lead'].search([('stage_id', '=', 6)])
            op_eco_particip_ids = []

            for obj in lead_ids:
                print 'obj',obj
                partner_id = obj.partner_id.id
                email_partner=self.env['res.partner'].browse(partner_id).email
                print 'Partenaire email: ',email_partner
                if email_partner != False :

                    list_mail.append(str(email_partner)+',')
                    self.multi_email = list_mail
                    print 'Les emails :',self.multi_email

                    list_partner.append(partner_id)
                    print 'Les partenaires: ',list_partner

                    self.recipient_ids = [(6, 0, list_partner)]


        if self.filter_type == 'etat_adhesion':

            if self.etat_adhesion == "membre_payant":
                op_eco_ids = self.env['res.partner'].search([('membership_state', '=', 'paid')])
                print 'if op_eco_ids ....',op_eco_ids
            elif self.etat_adhesion == "autre":
                op_eco_ids = self.env['res.partner'].search([('membership_state', '!=', 'paid')])
                print 'elif op_eco_ids ....',op_eco_ids
            else:
                op_eco_ids = self.env['res.partner'].search([])
                print 'else op_eco_ids ....',op_eco_ids

            for obj in op_eco_ids:
                partner_id = obj.id
                print '',partner_id
                email_partner=self.env['res.partner'].browse(partner_id).email
                if email_partner != False :
                    #p.agent_info = u' '.join((agent_contact, agent_telno)).encode('utf-8').strip()
                    email=((str(email_partner)).encode('utf-8')+',').encode('utf-8')

                    self.multi_email = self.multi_email + email
                    print 'self.multi_email..',self.multi_email
                    list_partner.append(partner_id)
                    self.recipient_ids = [(6, 0, list_partner)]

        secteur_activite_ids = []
        for sec_act_obj in self.secteur_activite:
            secteur_activite_ids.append(sec_act_obj.id)

        if self.filter_type == 'secteur_activite':
            print 'secteur_activite_ids ...',secteur_activite_ids
            all_op_eco_ids = []
            if self.secteur_activite:
                for sec_act_id in secteur_activite_ids:
                    self.env.cr.execute('SELECT partner_id FROM res_partner_res_partner_category_rel WHERE category_id =' + str(sec_act_id))
                    # cr.execute('SELECT r.partner_id FROM res_partner r,res_partner_res_partner_category_rel c WHERE c.category_id =' + str(sec_act_id) + ' AND c.partner_id = r.id AND r.is_company = True ')
                    res = self.env.cr.fetchall()
                    op_eco_ids = [x[0] for x in res]
                    all_op_eco_ids.extend(op_eco_ids)
                    print '.......', list(set(all_op_eco_ids))

                for partner_id in list(set(all_op_eco_ids)):
                    print '',partner_id
                    email_partner=self.env['res.partner'].browse(partner_id).email
                    if email_partner != False :
                        #p.agent_info = u' '.join((agent_contact, agent_telno)).encode('utf-8').strip()
                        email=(str(email_partner)).encode('utf-8')+','
                        self.multi_email = self.multi_email + email
                        print 'self.multi_email..',self.multi_email
                        list_partner.append(partner_id)
                        self.recipient_ids = [(6, 0, list_partner)]
            else:
                self.env.cr.execute('SELECT DISTINCT(partner_id) FROM res_partner_res_partner_category_rel')
                res = self.env.cr.fetchall()
                op_eco_ids = [x[0] for x in res]
                for partner_id in op_eco_ids:
                    print '', partner_id
                    email_partner = self.env['res.partner'].browse(partner_id).email
                    if email_partner != False:
                        # p.agent_info = u' '.join((agent_contact, agent_telno)).encode('utf-8').strip()
                        email = (str(email_partner)).encode('utf-8') + ','
                        self.multi_email = self.multi_email + email
                        print 'self.multi_email..', self.multi_email
                        list_partner.append(partner_id)
                        self.recipient_ids = [(6, 0, list_partner)]

        elif self.filter_type == 'group':

            if self.group_id:
                self.env.cr.execute('SELECT partner_id FROM group_partner_rel WHERE group_id =' + str(self.group_id.id, ))
                res = self.env.cr.fetchall()
                print 'resultat :', res
                op_eco_ids = [x[0] for x in res]
                for partner_id in op_eco_ids:
                    print '', partner_id
                    email_partner = self.env['res.partner'].browse(partner_id).email
                    if email_partner != False:
                        # p.agent_info = u' '.join((agent_contact, agent_telno)).encode('utf-8').strip()
                        email = (str(email_partner)).encode('utf-8') + ','
                        self.multi_email = self.multi_email + email
                        print 'self.multi_email..', self.multi_email
                        list_partner.append(partner_id)
                        self.recipient_ids = [(6, 0, list_partner)]

        # # update 20-09-2017 by marwa bm
        # mail_info = self.pool.get('mail.information').write(cr, uid, new_mail_info,
        #                                                     {'subject': '', 'type_menu': 'Adherent'},)


class survey_page(osv.Model):
    _name = 'survey.page'
    _inherit ='survey.page'

class survey_question(osv.Model):
    _name = 'survey.question'
    _inherit ='survey.question'


class survey_label(osv.Model):
    _name = 'survey.label'
    _inherit ='survey.label'

# class survey_mail_compose_message(osv.TransientModel):
#     _name = 'survey.mail.compose.message'
#     _inherit = 'survey.mail.compose.message'
