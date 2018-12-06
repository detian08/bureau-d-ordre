# -*- coding: utf-8 -*-
from openerp import models, fields, api
from cmislib import CmisClient, Repository, Folder
from cmislib.exceptions import CmisException
import tempfile
import base64


class upload_wizard(models.TransientModel):
    _name = 'office.document.alfresco.sale.wizard'
    chemin = fields.Binary(string=" ")
    nom_fichier = fields.Char(string="Nom du fichier", required="True", readonly=False)

    @api.multi
    def _get_active_id(self, context=None):
        return context.get('active_id', False)

    @api.multi
    def _get_name(self, context=None):
        return context.get('reference',False)

    @api.multi
    def _get_partner(self, context=None):
        partner_id = self._context.get('partner_id')
        return self.env['res.partner'].browse(partner_id).name


    @api.multi
    def upload_document(self):
        configs = self.env['office.alfresco.configuration'].search([('is_default', '=', 'True')])[0]
        url = configs.url
        port = configs.port
        user = configs.user
        mp = configs.mp
        try:
            client = CmisClient('http://' + url + ':' + repr(port) + '/alfresco/service/cmis', user, mp)
            repo = client.defaultRepository
        except:
            print "failed to connect to Alfresco"
            quit()

        repo = client.getDefaultRepository()
        root = repo.rootFolder
        try:
            Client = repo.getObjectByPath('/Clients')
        except:
            Client = root.createFolder('Clients')

        try:
            eFolder = repo.getObjectByPath('/Clients/' + self._get_name(self.env.context))
        except:
            eFolder = Client.createFolder(self._get_name(self.env.context))

        try:
            sFolder = repo.getObjectByPath('/Clients/' + self._get_name(self.env.context) + '/Bons de commande')
        except:
            sFolder = eFolder.createFolder('Bons de commande')
        #added by salwa ksila 06/04/2017
        data = base64.decodestring(self.chemin)
        # create a temporary file, and save the image
        fobj = tempfile.NamedTemporaryFile(delete=False)
        fname = fobj.name
        fobj.write(data)
        fobj.close()

        eContent = open(fname, 'r')
        eFile = sFolder.createDocument(self.nom_fichier, contentFile=eContent)

        self.env['office.document.alfresco.vente'].create({'node': eFile.id, 'nom_fichier':
            self.nom_fichier,'vente_id': self._get_active_id(self.env.context),
                                                           'nom_client': self._get_partner(self.env.context)})
