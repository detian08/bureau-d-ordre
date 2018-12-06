# -*- coding: utf-8 -*-
from __future__ import division
from openerp import models, fields, api

class iway_pfe(models.Model):
    _name = 'iway_entretien.iway_entretien'

    @api.multi
    def onchange_score(self):
	print "onchange .........evaluation_ids",self.browse().ids
        score=0.00
	list_critere = []
	somme_note=0
	somme_critere=0
	total_note=0

	
        note_obj = self.env['entretien_evaluation.entretien_evaluation']
        print 'note_obj........',note_obj
        for ent_id in self:#self contient la liste des ids des entretiens
#self.scorefinal ===> bug ===> sol :
        	print ".........entretien en cours", ent_id.id
		list_search =note_obj.search([('entretien_id','=',ent_id.id)])
		somme_critere=len(list_search)
		for critere_id in  list_search:
			print "critere......",critere_id
			note = note_obj.browse(critere_id.id).note
			total_note = total_note + int(note)
			print "total_note.....",total_note,'....',(somme_critere *100)
			score= total_note / (somme_critere * 100)
			ent_id.scorefinal=score
	#		list_critere.append(critere)
	#		somme_critere=somme_critere + list_critere.count(critere)
#		print "somme_critere......",somme_critere


        return True

    sujet = fields.Char(string="Sujet")
    #responsable = fields.Char(string="Responsable")
    #mail = fields.Char(string="EMAIL")
    #telephone = fields.Char(string="TELEPHONE")
    #description = fields.Char(string="Description")
    #categorie_echelon  = fields.Char(string="Catégorie échelon ")
    #competence = fields.Char(string="Compétence")
	#modif
    scorefinal = fields.Float(compute='onchange_score',string="Score Final",store=True)
    decision = fields.Char(string="Décision")
    localite = fields.Char(string="Localité")

    #date_pfe = fields.Date(string='Date_pfe', default=fields.Date.today(), )default=fields.Date.today()
    date_entretien = fields.Datetime(string='Date entretien',  )
    #date_fin_pfe = fields.Date(string='Date_fin_pfe', default=fields.Date.today(), )
    #detaille = fields.text(string="Détaille")
    #comment = fields.Text(string="Comment")
    observation = fields.Text(string="Observation")
    candidature_id = fields.Many2one(comodel_name="hr.applicant" , string="Candidatures")
    responsable = fields.Many2one('res.users', 'Responsable', track_visibility='onchange')
    #presentiel = fields.Boolean(string='Présentiel', default=_set_is_active)
    evaluation_ids = fields.One2many(comodel_name="entretien_evaluation.entretien_evaluation", string='Evaluation', inverse_name="entretien_id")
    mode = fields.Selection([('p', 'Présentiel'), ('a', 'à distance'),	
	 ], string='Mode')
    


#<!--Workflow-->  
    #attendees_count = fields.Integer(string="Attendees count", compute='_get_attendees_count', store=True)

    state = fields.Selection([
        ('brouillon', "Brouillon"),
        ('affecter', "Affecter"),
        ('cloture', "Cloturer"),
    ], default='brouillon', string="État")

    @api.multi
    def action_brouillon(self):
	print 'hello brouillon'
        self.state = 'brouillon'

    @api.multi
    def action_affecte(self):
	print 'hello affecte'
        self.state = 'affecter'

    @api.multi
    def action_cloture(self):
	print 'hello cloture'
        self.state = 'cloture'









