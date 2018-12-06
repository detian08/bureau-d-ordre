# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime, date
import time


class budget_budget(models.Model):
    _name = 'budget.budget'


    def _set_is_decede(self):
        # Write method
        return False


    #sequence refernce
    type_bgt = fields.Integer(string="Type budget")
    libelle_bgt = fields.Char(string="Libelle")
    type_piece = fields.Integer(string="Type pièce")
    name =fields.Char(string="Ref Piece")
    date_mise = fields.Date(string="Date Mise En Place")

    #employee_ids = fields.Many2one(comodel_name="hr.employee", string="Employés", required="True")
    #state = fields.Selection([('brouillon', 'Brouillon'), ('envoye', 'Envoyé'),  ('att_valid', 'En attente de validation'), ('valide', 'Validé'),('refuse', 'Refusé'),], string='Etat', default='brouillon')
    budget_line_ids = fields.One2many(string="Ligne budgetaire", comodel_name="budget.line", inverse_name="budget_id")


#******************************************budget line*******************
class budget_line(models.Model):
    _name = 'budget.line'
   
    

    budget_id = fields.Many2one(comodel_name="budget.budget", string="Budgets")
    titre = fields.Integer (string="Titre")
    section = fields.Integer(string="Section")
    chapitre = fields.Integer(string="Chapitre")
    article = fields.Integer(string="Article")
    paragraphe = fields.Integer(string="Paragraphe")
    dotation = fields.Float(string="Dotation")
    rubrique_line_ids = fields.One2many(string="Rubrique", comodel_name="rubrique.line", inverse_name="rubrique_id")


# ******************************************rubrique*******************
class rubrique_line(models.Model):
    _name = 'rubrique.line'

    rubrique_id = fields.Many2one(comodel_name="budget.line", string="Rubriques")
    code_rub = fields.Integer(string="Code")
    libelle = fields.Char(string="Libelle")
    an1 = fields.Integer(string="An : 2013")
    an2 = fields.Integer(string="An : 2014")
    an3 = fields.Integer(string="An : 2015")
    dotation = fields.Float(string="Dotation")



