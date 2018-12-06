# -*- coding: utf-8 -*-

from openerp import models, fields, api
import os
import tempfile
import base64


class upload_wizard(models.TransientModel):
	_name = 'office.document.alfresco.product.wizard'
	chemin = fields.Binary(string=" ")
	nom_fichier = fields.Char(string="Nom du fichier", required="True", readonly=False)

	@api.multi
	def _get_active_id(self ,context=None):
		return context.get('active_id', False)

	@api.multi
	def _get_cin(self ,context=None):
		return context.get('default_code', False)

	@api.multi
	def _get_title(self, context=None):
		return context.get('name', False)



	@api.multi
	def upload_document(self):
		repo = self.env['office.alfresco.configuration'].connection_alfresco()
		root = repo.rootFolder

		try:
			Produits = repo.getObjectByPath('/Produits')
		except:
			Produits = root.createFolder('Produits')

		try:
			sFolder = repo.getObjectByPath( '/Produits/' + self._get_cin(self.env.context))
		except:
			sFolder = Produits.createFolder(self._get_cin(self.env.context) )

		# added by salwa ksila 23/07/2017
		file_data = base64.decodestring(self.chemin)
		file_obj = tempfile.NamedTemporaryFile(delete=False)
		file_name = file_obj.name
		file_obj.write(file_data)
		file_obj.close()

		file_content = open(file_name, 'r')
		document = sFolder.createDocument(self.nom_fichier, contentFile=file_content)

		record = self.env['office.document.alfresco.produit'].create({'node': document.id, 'nom_fichier':
			self.nom_fichier, 'produit_id': self._get_active_id(self.env.context), })

