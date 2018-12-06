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
    connaissance = fields.Char(string="Connaissance")
    #date_pfe = fields.Date(string='Date_pfe', default=fields.Date.today(), )
    date_debut_pfe = fields.Date(string='Date début pfe', default=fields.Date.today(), )
    date_fin_pfe = fields.Date(string='Date fin pfe', default=fields.Date.today(), )
    #detaille = fields.text(string="Détaille")
    #stagiaire = fields.Char(string="Stagiaire")
    periode = fields.Char(string="Periode")
    directeur_technique = fields.Char(string="Directeur Technique")
    stagiaire = fields.Char(string="Stagiaire")
    cin = fields.Char(string="Cin")

    description = fields.Text(string="Description")
    profil_candidat = fields.Selection([('p', 'Ingeniorat'), ('a', 'Master'),('b', 'Licence'),	
	 ], string='Profil Candidat')

#champs ajouter
    cin = fields.Integer(string="Cin", help="This field shows the number of related cin")



    type_menu = fields.Selection([('pfe', 'PFE'), ('pfa', 'PFA'),
                            ('ste', 'STE'), ], string='Type')




#<!--Workflow-->  
    #attendees_count = fields.Integer(string="Attendees count", compute='_get_attendees_count', store=True)

    state = fields.Selection([
        ('propose', "Proposer"),
        ('affecter', "Affecter"),
        ('cloture', "Cloturer"),
    ], default='propose')

    @api.one
    @api.constrains('cin')
    def _check_cin(self):
	print ".................", self.cin
	print '..............',type(self.cin)
	if len(str(self.cin)) > 8:
		raise Warning('The max is 8, you can not add the third!')

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
###PFA###

    sujet = fields.Char(string="Sujet")
    #prenom = fields.Char(string="PRENOM")
    #mail = fields.Char(string="EMAIL")
    #telephone = fields.Char(string="TELEPHONE")
    #description = fields.Char(string="Description")
    reference = fields.Char(string="Référence")
    competence = fields.Char(string="Compétence")
    #date_pfe = fields.Date(string='Date_pfe', default=fields.Date.today(), )
    date_debut_pfe = fields.Date(string='Date début stage', default=fields.Date.today(), )
    date_fin_pfe = fields.Date(string='Date fin stage', default=fields.Date.today(), )
    #detaille = fields.text(string="Détaille")
    description = fields.Text(string="Description")
    duree = fields.Char(string="Durée")
    encadreur = fields.Char(string="Encadreur")
    


#<!--Workflow-->  
    #attendees_count = fields.Integer(string="Attendees count", compute='_get_attendees_count', store=True)

    state = fields.Selection([
        ('propose', "Proposer"),
        ('affecter', "Affecter"),
        ('cloture', "Cloturer"),
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
###STE###

    sujet = fields.Char(string="Sujet")
    #prenom = fields.Char(string="PRENOM")
    #mail = fields.Char(string="EMAIL")
    #telephone = fields.Char(string="TELEPHONE")
    #description = fields.Char(string="Description")
    reference = fields.Char(string="Référence")
    competence = fields.Char(string="Compétence")
    #date_pfe = fields.Date(string='Date_pfe', default=fields.Date.today(), )
    date_debut_pfe = fields.Date(string='Date début Stage', default=fields.Date.today(), )
    date_fin_pfe = fields.Date(string='Date fin Stage', default=fields.Date.today(), )
    #detaille = fields.text(string="Détaille")
    description = fields.Text(string="Description")
    duree = fields.Char(string="Durée")
    encadreur = fields.Char(string="Encadreur")
    periode = fields.Char(string="Periode")
    profil_condidat = fields.Char(string="Profil Candidat")
    


#<!--Workflow-->  
    #attendees_count = fields.Integer(string="Attendees count", compute='_get_attendees_count', store=True)

    state = fields.Selection([
        ('propose', "Proposer"),
        ('affecter', "Affecter"),
        ('cloture', "Cloturer"),
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











