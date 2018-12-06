# -*- coding: utf-8 -*-

from openerp import models, fields, api

class courriel_degre(models.Model):
	_name = 'courriel.degre'

	name =fields.Char(string="degrés de confidentialité")


