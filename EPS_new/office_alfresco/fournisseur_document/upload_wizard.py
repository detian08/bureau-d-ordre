# -*- coding: utf-8 -*-
from openerp import models, fields, api
import tempfile
import base64
import os


class upload_wizard(models.TransientModel):
	_name = 'office.document.alfresco.fournisseur.wizard'
	chemin = fields.Binary(string=" ")
	nom_fichier = fields.Char(string="Nom du fichier", required="True", readonly=False)

	@api.multi
	def _get_active_id(self, context=None):
		return self._context.get('active_id', False)

	@api.multi
	def _get_name(self, context=None):
		return self._context.get('reference')

	@api.multi
	def _get_partner(self, context=None):
		partner_id = self._context.get('partner_id')
		return self.env['res.partner'].browse(partner_id).name

	@api.multi
	def _get_partner_id(self, context=None):
		return self._context.get('partner_id')

	@api.multi
	def upload_document(self):
		repo = self.env['office.alfresco.configuration'].connection_alfresco()
		root = repo.rootFolder

		print "partner========",self._get_partner(self.env.context)

		try:
			Fournisseurs = repo.getObjectByPath('/Fournisseurs')
		except:
			Fournisseurs = root.createFolder('Fournisseurs')

		try:
			eFolder = repo.getObjectByPath('/Fournisseurs/' + self._get_partner(self.env.context))
		except:
			eFolder = Fournisseurs.createFolder(self._get_partner(self.env.context))

		try:
			sFolder = repo.getObjectByPath('/Fournisseurs/' + self._get_partner(self.env.context) + '/Factures')
		except:
			sFolder = eFolder.createFolder('Factures')

		# try:
		# 	dossier_facture = repo.getObjectByPath('/Fournisseurs/' + self._get_partner(self.env.context)+ '/Factures/'+ repr(self._get_active_id(self.env.context)))
		#
		# except:
		# 	dossier_facture = sFolder.createFolder(repr(self._get_active_id(self.env.context)))

		# added by salwa ksila 23/07/2017
		file_data = base64.decodestring(self.chemin)
		file_obj = tempfile.NamedTemporaryFile(delete=False)
		file_name = file_obj.name
		file_obj.write(file_data)
		file_obj.close()

		file_content = open(file_name, 'r')

		document = sFolder.createDocument(self.nom_fichier, contentFile=file_content)

		self.env['office.document.alfresco.fournisseur'].create({'node' : document.id ,'nom_fichier':
			self.nom_fichier ,'ref_facture' : self._get_active_id(self.env.context),'partner_id':self._get_partner_id(self.env.context)})