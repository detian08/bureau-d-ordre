# -*- coding: utf-8 -*-
import os
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import sys

import tempfile
import base64
from openerp import models, fields, api
from cmislib import CmisClient, Repository, Folder

sys.path.append(os.path.abspath("/home/habid/odoo_ERP/CRM_CCI/cci_messaging"))


class documentMessage(models.Model):

    _name = 'cci.document.alfresco.message'

    node = fields.Char(required=True)
    nom_fichier = fields.Char(required=True)
    description = fields.Text()
    message_id = fields.Many2one('cci.messaging',ondelete='cascade')

    @api.multi
    def unlink(self):
        repo = self.env['cci.alfresco.configuration'].connection_alfresco()
        try:
            doc = repo.getObject(self.node)
            doc.delete()
        except:
            pass
        finally:
            models.Model.unlink(self)


    @api.multi
    def download_document(self):
        repo = self.env['cci.alfresco.configuration'].connection_alfresco()

        doc = repo.getObject(self.node)
        doc_content = doc.getContentStream()

        file_obj = tempfile.NamedTemporaryFile(delete=False)
        file_name = file_obj.name
        file_obj.write(doc_content.read())
        file_obj.close()

        file_base64 = ''
        with open(file_name, "rb") as file:
            file_base64 = base64.encodestring(file.read())


        download_wizard_record = self.env['cci.download.wizard'].create({'download_link' :file_base64 ,'nom_fichier':self.nom_fichier})


        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cci.download.wizard',
            'res_id': int(download_wizard_record),
            'type': 'ir.actions.act_window',
            'target': 'new',
        }


class messaging(models.Model):
    _inherit = 'cci.messaging'

    message_documents_ids = fields.One2many('cci.document.alfresco.message', 'message_id', string='Documents')

    @api.multi
    def _get_active_id(self, context=None):
        return context.get('active_id', False)


    @api.multi
    def ajout(self):
        return {
            'name': "Les documents des emails internes",
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cci.document.alfresco.message.wizard',
            'view_id ref="wizard_form_view5"': True,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
