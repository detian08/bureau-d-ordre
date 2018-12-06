# -*- encoding: utf-8 -*-

from openerp import models, fields, api
from random import randint
from openerp.exceptions import ValidationError

from cmislib import CmisClient, Repository, Folder
from cmislib.model import CmisId
from cmislib.exceptions import CmisException, UpdateConflictException
import os, sys
import subprocess
import time, datetime

class Alfresco_configuration(models.Model):
	_name = 'office.alfresco.configuration'

	url = fields.Char(string="Alfresco url", required=True)
	port = fields.Integer(string="Port", required=True)
	user = fields.Char(string="Nom d'utilisateur", required=True)
	mp = fields.Char(string="Mot de passe", required=True)
	is_default = fields.Boolean(string="Utiliser par default")

	@api.model
	def create(self, vals):
		default_exists = self.env['office.alfresco.configuration'].search([('is_default', '=', 'True')], limit=1).id
		if default_exists and vals['is_default']:
			raise ValidationError(u'Une seule configuration par defaut est possible !')
		else:
			rec = super(Alfresco_configuration, self).create(vals)
			return rec

	@api.multi
	def write(self, vals):
		default_exists = self.env['office.alfresco.configuration'].search(
			[('is_default', '=', 'True'), ('id', '!=', self.id)], limit=1).id
		if default_exists and vals['is_default']:
			raise ValidationError(u'Une seule configuration par défault est possible !')
		else:
			return super(Alfresco_configuration, self).write(vals)

	@api.multi
	def connection_alfresco(self):
		try:
			configs = self.env['office.alfresco.configuration'].search([('is_default', '=', 'True')])[0]
		except:
			raise ValidationError(u'Veuillez configurer la connexion à Alfresco !')
		url = configs.url
		port = configs.port
		user = configs.user
		mp = configs.mp
		try:
			client = CmisClient('http://' + url + ':' + repr(port) + '/alfresco/service/cmis', user, mp)
			repo = client.defaultRepository
			return repo
		except:
			raise ValidationError(u'Erreur de connexion à Alfresco, Veuillez vérifier les paramètres fournis !')

	@api.multi
	def config_test(self):
		try:
			configs = self.env['office.alfresco.configuration'].search([('is_default', '=', 'True')])[0]
		except:
			raise ValidationError(u'Veuillez configurer la connexion à Alfresco !')

		url = configs.url
		port = configs.port
		user = configs.user
		mp = configs.mp
		try:
			client = CmisClient('http://' + url + ':' + repr(port) + '/alfresco/service/cmis', user, mp)
			repo = client.defaultRepository
			return self.env['warning_box'].info('', 'Connexion établie !')
		except:
			raise ValidationError(u'Erreur de connexion à Alfresco, Veuillez vérifier les paramètres fournis !')
