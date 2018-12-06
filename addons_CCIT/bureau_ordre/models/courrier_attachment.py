# -*- coding: utf-8 -*-

import pprint
from openerp.osv import fields, osv
from openerp import models, fields, api
from random import randint
from openerp.exceptions import ValidationError

from cmislib import CmisClient, Repository, Folder
#from cmislib.model import CmisId
from cmislib.exceptions import CmisException, UpdateConflictException
import os, sys
import subprocess
import time, datetime

class alfresco_configuration(osv.Model):
    _name = "alfresco.configuration"

    _columns ={
        'url' : fields.char(string="Alfresco url", required=True),
        'port' : fields.integer(string="Port", required=True),
        'user' : fields.char(string="Nom d'utilisateur", required=True),
        'mp' : fields.char(string="Mot de passe", required=True),
        'is_default' : fields.boolean(string="Utiliser par default")
    }

class attachment_courrier(osv.Model):
    _name = "document.attachment"

    _columns = {
        'node': fields.char(required=True, readonly=True),
        'nom_fichier': fields.char("Nom du fichier", required=True),
        'description': fields.text("Description"),
        'courrier_id': fields.many2one('document.courrier', "Produit"),
    }

    def download_document(self, cr, uid, ids, context=None):
        active_record = self.browse(cr, uid, ids[0], context=context)

        configs = self.pool.get('alfresco.configuration').search(cr, uid, [('is_default', '=', 'True')],
                                                                 context=context)
        config = self.pool.get('alfresco.configuration').browse(cr, uid, configs, context=context)[0]

        url = config.url
        port = config.port
        user = config.user
        mp = config.mp
        try:
            client = CmisClient('http://' + url + ':' + repr(port) + '/alfresco/service/cmis', user, mp)
            repo = client.getDefaultRepository()
        except:
            raise ValidationError(u'Erreur de connexion à Alfresco, Veuillez vérifier les paramètres fournis !')


        doc = repo.getObject(active_record.node)
        doc_content = doc.getContentStream()

        file_obj = tempfile.NamedTemporaryFile(delete=False)
        file_name = file_obj.name
        file_obj.write(doc_content.read())
        file_obj.close()

        file_base64 = ''
        with open(file_name, "rb") as file:
            file_base64 = base64.encodestring(file.read())


        download_wizard_record = self.pool.get('document.attachment.download.wizard').create(cr,uid,{'download_link' :file_base64 ,'nom_fichier':active_record.nom_fichier})

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'document.attachment.download.wizard',
            'res_id': int(download_wizard_record),
            'type': 'ir.actions.act_window',
            'target': 'new',
        }


class upload_wizard(osv.TransientModel):
    _name = 'document.attachment.upload.wizard'

    _columns = {
        'chemin': fields.binary("Chemin"),
        'nom_fichier': fields.char("Nom du fichier", required="True", readonly=False),
        'description': fields.text("Description"),
    }

    def _get_reference(self, cr, uid, ids, context=None):
        active_courrier_id = context.get('active_id')
        active_courrier_reference = self.pool.get('document.courrier').browse(cr, uid, active_courrier_id, context=context).name
        return active_courrier_reference


    def upload_document(self, cr, uid, ids, context=None):
        active_wizard = self.browse(cr, uid, ids[0], context=context)

        active_courrier_id = context.get('active_id')
        active_courrier_reference = self.pool.get('document.courrier').browse(cr, uid, active_courrier_id,
                                                                              context=context).name

        configs = self.pool.get('alfresco.configuration').search(cr, uid, [('is_default', '=', 'True')],
                                                                     context=context)
        config = self.pool.get('alfresco.configuration').browse(cr, uid, configs, context=context)[0]

        url = config.url
        port = config.port
        user = config.user
        mp = config.mp
        try:
            client = CmisClient('http://' + url + ':' + repr(port) + '/alfresco/service/cmis', user, mp)
            repo = client.getDefaultRepository()
            root = repo.rootFolder
        except:
            raise ValidationError(u'Erreur de connexion à Alfresco, Veuillez vérifier les paramètres fournis !')

        try:
            courriers_folder = repo.getObjectByPath('/Courriers')
        except:
            courriers_folder = root.createFolder('Courriers')

        try:
            email_folder = repo.getObjectByPath('/Courriers/' + active_courrier_reference)
        except:
            email_folder = courriers_folder.createFolder(active_courrier_reference)

        file_data = base64.decodestring(active_wizard.chemin)
        file_obj = tempfile.NamedTemporaryFile(delete=False)
        file_name = file_obj.name
        file_obj.write(file_data)
        file_obj.close()

        file_content = open(file_name, 'r')
        document = email_folder.createDocument(active_wizard.nom_fichier, contentFile=file_content)

        record = self.pool.get('document.attachment').create(cr, uid,{'node': document.id, 'nom_fichier':
            active_wizard.nom_fichier,'description':active_wizard.description, 'courrier_id': int(context.get('active_id')), })

class download_wizard(osv.TransientModel):
    _name = 'document.attachment.download.wizard'

    _columns = {
        'download_link' : fields.binary(),
        'nom_fichier' : fields.char(),
    }
