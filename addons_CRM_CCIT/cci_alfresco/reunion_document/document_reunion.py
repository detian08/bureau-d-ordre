# -*- coding: utf-8 -*-
import os
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
from openerp import models, fields, api


from cmislib import CmisClient, Repository, Folder

class Document_reunion(models.Model):
    _name = 'cci.document.alfresco.reunion'

    node = fields.Char(required=True)
    nom_fichier = fields.Char(required=True)
    description = fields.Text()

    reunion_id = fields.Many2one('calendar.event',ondelete='cascade' )

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


class product(models.Model):
    _name='calendar.event'
    _inherit = 'calendar.event'

    document_ids = fields.One2many('cci.document.alfresco.reunion', 'reunion_id', string='Documents')


    # Marwa BM update 30/06/2017
    @api.multi
    def ajout(self):
        return {
            'name': "Les documents des réunions",
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cci.document.alfresco.reunion.wizard',
            'view_id ref="wizard_form_view2"': True,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
