# -*- coding: utf-8 -*-

from openerp import models, fields, api

class courriel_important(models.Model):
	_name = 'courriel.important'

	name =fields.Char(string="Importance")


