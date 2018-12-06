# -*- coding: utf-8 -*-
import time
from openerp.osv import fields, osv
import base64
import tempfile
import logging
from email.utils import formataddr
from urlparse import urljoin

import psycopg2
import pprint
from openerp import api, tools
from openerp import SUPERUSER_ID
from openerp.addons.base.ir.ir_mail_server import MailDeliveryException
from openerp.tools.safe_eval import safe_eval as eval
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class document_courrier(osv.Model):
    _name = 'document.courrier'
    _description = 'Courriel entrant '

    def _get_full_name(self, cr, uid, ids, name, args, context=None):
        result ={}
        for action_obj in self.browse(cr, uid, ids, context=context):
            result[action_obj.id] = action_obj.nom_expediteur + " " + action_obj.prenom_expediteur
            return result

    _columns = {
        'name': fields.char('Reference interne', readonly=True),
        'subject': fields.char('Objet', required=True),
        'nom_expediteur': fields.char('Nom expéditeur',required=True),
        'prenom_expediteur': fields.char('Prénom expéditeur',required=True),
        'expediteur':fields.function(_get_full_name,string='Expéditeur',type="char",store=True),
        'cin_expediteur': fields.char('cin', size=8),
        'adresse': fields.text('Adresse'),
        'mode_envoi': fields.many2one("document.transmission.categ", 'Mode Transmission', ),
        'date_envoi': fields.date('Date Envoi'),
        'date_reception': fields.date('Date Reception'),

        'categorie': fields.many2one("document.category", 'Type Document', ),
        'priorite': fields.selection([('haute', 'Haute'), ('moyenne', 'Moyenne'), ('basse', u'Basse')], 'priorite'),

        'details': fields.text('Detail'),

        'date_sauv_courrier': fields.date('Date Enregistrement Courrier', readonly=True),
        'date_envoie_courrier': fields.date('Date Envoie Courrier'),
        'date_reception_courrier': fields.date('Date Reception Courrier'),
        'date_reply_courrier': fields.date('Date Reply Courrier'),
        'date_limite': fields.date('Date Limite'),

        'reponse': fields.text('Reponse'),
        'state': fields.selection(
            [('draft', 'Brouillon'), ('processed', 'En cours de traitement'), ('done', u'Clôturé')],
            'State', readonly=True),
        'courrier_actions': fields.one2many('document.action', 'courrier_id', 'Actions Courrier', ondelete='cascade'),
        #'attachments_ids': fields.one2many('document.attachment', 'courrier_id', 'Actions Courrier'),
        'prochain_destinataire': fields.many2one('res.users', 'Destinataire', readonly=True),
    }

    def message_redirect_action(self, cr, uid, context=None):
        """ For a given message, return an action that either
            - opens the form view of the related document if model, res_id, and
              read access to the document
            - opens the Inbox with a default search on the conversation if model,
              res_id
            - opens the Inbox with context propagated

        """

        if context is None:
            context = {}
        # super(subClass, instance).method(args)
        action = self.pool.get('mail.thread').message_redirect_action(cr, uid, context=context)
        return action

    _defaults = {
        'state': 'draft',
        'date_sauv_courrier': time.strftime('%Y-%m-%d'),
    }

    def create(self, cr, uid, vals, context=None):
        vals['name'] = self.pool.get('ir.sequence').next_by_code(cr, uid,'document.courrier')
        return super(document_courrier, self).create(cr, uid, vals, context)

    def action_draft(self, cr, uid, ids, context=None):
        for action_obj in self.browse(cr, uid, ids, context=context):
            action_obj.write({'state': 'draft'})
        return True

    def action_send(self, cr, uid, ids, context=None):
        wizard_action_transfert_view_id = \
        self.pool.get('ir.ui.view').search(cr, uid, [('name', '=', 'document.action.transfert.wizard.form')], context=context)[
            0]

        return {
            'name': u'Transférer un courrier',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'document.action',
            'view_id': wizard_action_transfert_view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',

        }

    def action_done(self, cr, uid, ids, context=None):
        wizard_action_cloturer_view_id = self.pool.get('ir.ui.view').search(cr, uid, [('name', '=', 'document.action.cloturer.wizard.form')], context=context)[0]

        return {
            'name': u'Donner une réponse définitive',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'document.action',
            'view_id': wizard_action_cloturer_view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def add_attachment(self, cr, uid, ids, context=None):
        for action_obj in self.browse(cr, uid, ids, context=context):
            return {
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'document.attachment.upload.wizard',
                'view_id ref="upload_wizard_view_form"': True,
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context': context
            }


document_courrier()


class document_transmission_categ(osv.osv):
    _name = "document.transmission.categ"

    _columns = {
        'code': fields.char('code', size=64, ),
        'name': fields.char("name", size=250, ),
    }


document_transmission_categ()


class document_category(osv.osv):
    _name = "document.category"

    _columns = {
        'code': fields.char('code', size=64, ),
        'name': fields.char("name", size=250, ),
    }


document_category()


class document_action(osv.osv):
    _name = "document.action"

    _columns = {
        'name': fields.char("name", size=250, ),
        'courrier_id': fields.many2one("document.courrier", 'Courrier', ),
        'from': fields.many2one("res.users", 'Expediteur'),
        'to': fields.many2one('res.users', 'Destinataire'),
        'date_action': fields.date('Date Action'),
        'message': fields.text('Message'),
        'type_action': fields.selection([('fin', u'Réponse définitive'), ('transfert', u'Transférer')]),
        'reponse_type': fields.selection(
            [('accepte', u'Accepté'), ('refuse', u'Refusé'), ('manque', u'Documents manquants')]),
    }

    _defaults = {
        'type_action': lambda *a: 'transfert',
        'date_action': time.strftime('%Y-%m-%d'),
        'from': lambda s, c, u, ctx: u,
    }

    def action_send(self, cr, uid, ids, context=None):
        courrier_obj = self.pool.get('document.courrier').browse(cr, uid, int(context.get('courrier_id', False)), context=context)
        active_user = self.pool.get('res.users').browse(cr, uid, uid, context=context).partner_id

        for action_obj in self.browse(cr, uid, ids, context=context):
            action_obj.write(
                {'type_action': 'transfert', 'courrier_id': int(context.get('courrier_id', False)),
                 'prochain_destinataire': int(action_obj.to.id), 'from': uid})
            action_obj.courrier_id.write({'state': 'processed'})

            message_vals = {
                'subject': courrier_obj.subject,
                'body': u'<html> ' + str(action_obj.message) + ' </html>',
                'record_name': u'Courrier transféré',
                'res_id': courrier_obj.id,
                'author_id': active_user.id,
                'model': 'document.courrier',
                'type': 'notification',
                'email_from': active_user.name,
                'starred': True,
            }

            transfert_message = self.pool.get('mail.message').create(cr, uid, message_vals, context=context)

            recipient_id = self.pool.get('res.users').browse(cr, uid, action_obj.to.id, context=context).partner_id.id

            mail_notif_vals = {
                'partner_id': recipient_id,
                'message_id': transfert_message,
                'is_read': False,
                'starred': True,
            }
            action_obj.courrier_id.write({'prochain_destinataire': action_obj.to.id})

            self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)
        return True

    def action_done(self, cr, uid, ids, context=None):
        for action_obj in self.browse(cr, uid, ids, context=context):
            action_obj.write(
                {'type_action': 'fin', 'courrier_id': int(context.get('courrier_id', False)),})

            action_obj.courrier_id.write({'state': 'done'})

        return True


document_action()
