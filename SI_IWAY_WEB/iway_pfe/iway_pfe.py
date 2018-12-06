# -*- coding: utf-8 -*-

from openerp import models, fields, api

class iway_pfe(models.Model):
    _name = 'iway_pfe.iway_pfe'

    sujet = fields.Char(string="Sujet")
    #prenom = fields.Char(string="PRENOM")
    #mail = fields.Char(string="EMAIL")
    #telephone = fields.Char(string="TELEPHONE")
    #description = fields.Char(string="Description")
    reference = fields.Char(string="Référence")
    competence = fields.Char(string="Compétence")
    #date_pfe = fields.Date(string='Date_pfe', default=fields.Date.today(), )
    date_debut_pfe = fields.Date(string='Date début pfe', default=fields.Date.today(), )
    date_fin_pfe = fields.Date(string='Date fin pfe', default=fields.Date.today(), )
    #detaille = fields.text(string="Détaille")
    comment = fields.Text(string="Comment")
    


#<!--Workflow-->  
    #attendees_count = fields.Integer(string="Attendees count", compute='_get_attendees_count', store=True)

    state = fields.Selection([
        ('propose', "Proposé"),
        ('affecter', "Affecté"),
        ('cloture', "Cloturé"),
    ], default='propose')

    @api.multi
    def action_propose(self):
	print 'hello propose'
        self.state = 'propose'

    @api.multi
    def action_affecte(self):
	print 'hello affecte'
        self.state = 'affecter'

    @api.multi
    def action_cloture(self):
	print 'hello cloture'
        self.state = 'cloture'

   # @api.depends('seats', 'attendee_ids')
    #def _taken_seats(self):
        #for r in self:








