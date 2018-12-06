# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime, date
import time


class budget_budget(models.Model):
    _name = 'account.budget.post'
    _inherit="account.budget.post" #Budget



  #sequence refernce
    titre = fields.Char(string="Titre")
    section = fields.Char(string="Section")
    chapitre = fields.Char(string="chapitre")
    article =fields.Char(string="article")
    paragraphe = fields.Char(string="paragraphe")


   
