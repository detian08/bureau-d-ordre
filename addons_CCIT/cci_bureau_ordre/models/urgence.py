# -*- coding: utf-8 -*-

from openerp import models, fields, api

class courriel_urgence(models.Model):
	_name = 'courriel.urgence'

	name =fields.Char(string="urgence")


