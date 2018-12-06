# -*- coding: utf-8 -*-

import base64
import logging
import psycopg2
import tempfile
from email.utils import formataddr
from urlparse import urljoin

from cmislib.model import CmisClient

from openerp import SUPERUSER_ID
from openerp import api, tools
from openerp.addons.base.ir.ir_mail_server import MailDeliveryException
from openerp.osv import fields, osv
from openerp.tools.safe_eval import safe_eval as eval
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class mail_information(osv.Model):
	""" Model holding RFC2822 email messages to send. This model also provides
		facilities to queue and send new email messages.  """
	_name = 'mail.information'
	_description = 'Outgoing Mails'
	_inherits = {'mail.message': 'mail_message_information_id'}
	_order = 'id desc'
	_rec_name = 'subject'

	def _get_coach_id(self, cr, uid, ids, field_name, arg, context=None):
		print 'u will call get coach_id'
		res = {}
		for user in self.browse(cr, uid, ids, context=context):
			print 'user .....',ids
			partner_id = self.browse(cr, uid, ids, context=context).author_id.id
			print 'partner_id', partner_id
			user_id=self.pool.get('res.users').search(cr,uid,[('partner_id','=',partner_id)],context=context)[0]
			print 'user_id', user_id
			section_ids = self.pool.get('crm.case.section').search(cr, uid, [('member_ids', '=', user_id)],context=context)[0]

			if not section_ids:
				print 'nooooooooo'
				res[user.id] = 0
			else:
				print 'section_ids', section_ids
				coach_id = self.pool.get('crm.case.section').browse(cr, uid, section_ids, context=context).user_id.id
				print 'coach_id', coach_id
				res[user.id] = coach_id

		return res

	_columns = {
		'mail_message_information_id': fields.many2one('mail.message', 'Message', required=True, ondelete='cascade',
													   auto_join=True),
		'state': fields.selection([
			('outgoing', 'Sortant'),
			('sent', 'Envoyé'),
			('received', 'Reçu'),
			('exception', "Échec de l'envoi"),
			('cancel', 'Annulé'),
		], 'Status', readonly=True, copy=False),
		'auto_delete': fields.boolean('Suppression automatique',
									  help="Permanently delete this email after sending it, to save space"),
		'references': fields.text('Références', help='Message references, such as identifiers of previous messages',
								  readonly=1),
		'email_to': fields.text('À', help='Message recipients (emails)'),
		'recipient_ids': fields.many2many('res.partner', string='À (Partenaires)'),
		'email_cc': fields.char('Cc', help='Carbon copy message recipients'),
		#------envoi en cci-----
		'email_bcc': fields.char('Cci'),
		#-----------------------
		'body_html': fields.html('Rich-text Contents', help="Rich-text/HTML message"),
		'headers': fields.text('Entêtes ', copy=False),
		# Auto-detected based on create() - if 'mail_message_information_id' was passed then this mail is a notification
		# and during unlink() we will not cascade delete the parent and its attachments
		'notification': fields.boolean('Est une notification',
									   help='Mail has been created to notify people of an existing mail.message'),
		'type_menu': fields.selection([('Adherent', 'Adherent'), ('Nadherent', 'Nadherent')], 'Type', select=True,
									  change_default=True),
	'coach_id': fields.function(_get_coach_id, type="integer"),
	}

	_defaults = {
		'state': 'outgoing',
		'type_menu': 'Adherent',
		'email_to': ''
	}
	#Commenter par marwa bm le 20-09-2017 @vérifier
	#def recipient_ids_change(self, cr, uid, ids, dest_ids, context=None):
	#	result = {}
	#	if dest_ids:
	#		mail_obj = self.browse(cr, uid, ids, context=context)
	#		partner_list = mail_obj.recipient_ids
	#		mail_list = ''
	#		for part in dest_ids[0][2]:
	#			courriel = self.pool.get('res.partner').browse(cr, uid, part, context=context).email
	#			if mail_list == '':
	#				mail_list = courriel
	#			else:
	#				mail_list = mail_list + ',' + courriel
	#		result = {'value': {'email_to': mail_list}}
	#	return result

	def default_get(self, cr, uid, fields, context=None):
		# protection for `default_type` values leaking from menu action context (e.g. for invoices)
		# To remove when automatic context propagation is removed in web client
		if context and context.get('default_type') and context.get('default_type') not in self._all_columns[
			'type'].column.selection:
			context = dict(context, default_type=None)
		return super(mail_information, self).default_get(cr, uid, fields, context=context)

	def create(self, cr, uid, values, context=None):
		# notification field: if not set, set if mail comes from an existing mail.message
		values['type_menu'] = context.get('type_menu')
		if 'notification' not in values and values.get('mail_message_information_id'):
			values['notification'] = True
		return super(mail_information, self).create(cr, uid, values, context=context)

	def unlink(self, cr, uid, ids, context=None):
		# cascade-delete the parent message for all mails that are not created for a notification
		ids_to_cascade = self.search(cr, uid, [('notification', '=', False), ('id', 'in', ids)])
		parent_msg_ids = [m.mail_message_information_id.id for m in
						  self.browse(cr, uid, ids_to_cascade, context=context)]
		res = super(mail_information, self).unlink(cr, uid, ids, context=context)
		self.pool.get('mail.message').unlink(cr, uid, parent_msg_ids, context=context)
		return res

	def mark_outgoing(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'state': 'outgoing'}, context=context)

	def cancel(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)

	@api.cr_uid
	def process_email_queue(self, cr, uid, ids=None, context=None):
		"""Send immediately queued messages, committing after each
		   message is sent - this is not transactional and should
		   not be called during another transaction!

		   :param list ids: optional list of emails ids to send. If passed
							no search is performed, and these ids are used
							instead.
		   :param dict context: if a 'filters' key is present in context,
								this value will be used as an additional
								filter to further restrict the outgoing
								messages to send (by default all 'outgoing'
								messages are sent).
		"""
		if context is None:
			context = {}
		if not ids:
			filters = [('state', '=', 'outgoing')]
			if 'filters' in context:
				filters.extend(context['filters'])
			ids = self.search(cr, uid, filters, context=context)
		res = None
		try:
			# Force auto-commit - this is meant to be called by
			# the scheduler, and we can't allow rolling back the status
			# of previously sent emails!
			res = self.send(cr, uid, ids, auto_commit=True, context=context)
		except Exception:
			_logger.exception("Failed processing mail queue")
		return res

	def _postprocess_sent_message(self, cr, uid, mail, context=None, mail_sent=True):
		"""Perform any post-processing necessary after sending ``mail``
		successfully, including deleting it completely along with its
		attachment if the ``auto_delete`` flag of the mail was set.
		Overridden by subclasses for extra post-processing behaviors.

		:param browse_record mail: the mail that was just sent
		:return: True
		"""
		if mail_sent and mail.auto_delete:
			# done with SUPERUSER_ID to avoid giving large unlink access rights
			self.unlink(cr, SUPERUSER_ID, [mail.id], context=context)
		return True

	# ------------------------------------------------------
	# mail_information formatting, tools and send mechanism
	# ------------------------------------------------------

	def _get_partner_access_link(self, cr, uid, mail, partner=None, context=None):
		"""Generate URLs for links in mails: partner has access (is user):
		link to action_mail_redirect action that will redirect to doc or Inbox """
		if context is None:
			context = {}
		if partner and partner.user_ids:
			base_url = self.pool.get('ir.config_parameter').get_param(cr, SUPERUSER_ID, 'web.base.url')
			mail_model = mail.model or 'mail.thread'
			url = urljoin(base_url, self.pool[mail_model]._get_access_link(cr, uid, mail, partner, context=context))
			return "<span class='oe_mail_footer_access'><small>%(access_msg)s <a style='color:inherit' href='%(portal_link)s'>%(portal_msg)s</a></small></span>" % {
				'access_msg': _('about') if mail.record_name else _('access'),
				'portal_link': url,
				'portal_msg': '%s %s' % (context.get('model_name', ''), mail.record_name) if mail.record_name else _(
					'your messages'),
			}
		else:
			return None

	def send_get_mail_subject(self, cr, uid, mail, force=False, partner=None, context=None):
		"""If subject is void, set the subject as 'Re: <Resource>' or
		'Re: <mail.parent_id.subject>'

			:param boolean force: force the subject replacement
		"""
		if (force or not mail.subject) and mail.record_name:
			return 'Re: %s' % (mail.record_name)
		elif (force or not mail.subject) and mail.parent_id and mail.parent_id.subject:
			return 'Re: %s' % (mail.parent_id.subject)
		return mail.subject

	def send_get_mail_body(self, cr, uid, mail, partner=None, context=None):
		"""Return a specific ir_email body. The main purpose of this method
		is to be inherited to add custom content depending on some module."""
		body = mail.body_html

		# generate access links for notifications or emails linked to a specific document with auto threading
		link = None
		if mail.notification or (mail.model and mail.res_id and not mail.no_auto_thread):
			link = self._get_partner_access_link(cr, uid, mail, partner, context=context)
		if link:
			body = tools.append_content_to_html(body, link, plaintext=False, container_tag='div')
		return body

	def send_get_mail_to(self, cr, uid, mail, partner=None, context=None):
		"""Forge the email_to with the following heuristic:
		  - if 'partner', recipient specific (Partner Name <email>)
		  - else fallback on mail.email_to splitting """
		if partner:
			email_to = [formataddr((partner.name, partner.email))]
		else:
			email_to = tools.email_split_and_format(mail.email_to)
		return email_to

	def send_get_email_dict(self, cr, uid, mail, partner=None, context=None):
		"""Return a dictionary for specific email values, depending on a
		partner, or generic to the whole recipients given by mail.email_to.

			:param browse_record mail: mail.information browse_record
			:param browse_record partner: specific recipient partner
		"""
		body = self.send_get_mail_body(cr, uid, mail, partner=partner, context=context)
		body_alternative = tools.html2plaintext(body)
		res = {
			'body': body,
			'body_alternative': body_alternative,
			'subject': self.send_get_mail_subject(cr, uid, mail, partner=partner, context=context),
			'email_to': self.send_get_mail_to(cr, uid, mail, partner=partner, context=context),
		}
		return res

	def create_attachments(self, cr, uid, ids, context=None):
		# ---------récupération des pièces jointes de l'email --------
		active_record = self.browse(cr, uid, ids[0], context=context)
		active_record_attachments_ids = []
		active_record_attachments = None

		if active_record.type_menu == "Adherent":
			active_record_attachments_ids = self.pool.get('cci.document.oper.eco').search(cr, uid,
																						  [('ope_eco_id', "=",
																							active_record.id)]
																						  , context=context)
			if active_record_attachments_ids:
				active_record_attachments = self.pool.get('cci.document.oper.eco').browse(cr, uid,
																					  active_record_attachments_ids,
																					  context=context)
		else:
			active_record_attachments_ids = self.pool.get('cci.document.non.adherent').search(cr, uid,
																							  [('non_adh_id', "=",
																								active_record.id)]
																							  , context=context)
			if active_record_attachments_ids:
				active_record_attachments = self.pool.get('cci.document.non.adherent').browse(cr, uid,
																						  active_record_attachments_ids,
																						  context=context)

		if active_record_attachments:
			repo = self.pool.get('cci.alfresco.configuration').connection_alfresco_old_api(cr, uid, context=context)

			for attach in active_record_attachments:
				doc = repo.getObject(attach.node)
				result = doc.getContentStream()
				fobj = tempfile.NamedTemporaryFile(delete=False)
				fname = fobj.name
				fobj.write(result.read())
				fobj.close()

				with open(fname, "rb") as file:
					file_base64 = base64.encodestring(file.read())
					self.pool.get('ir.attachment').create(cr, uid, {'datas': file_base64, 'datas_fname': attach.nom_fichier,
																	'name': attach.nom_fichier,'res_model':active_record._name,
																	'res_id': active_record.id},
														  context=context)
			return True
		else:
			return False
	def send(self, cr, uid, ids, auto_commit=False, raise_exception=False, context=None):
		""" Sends the selected emails immediately, ignoring their current
			state (mails that have already been sent should not be passed
			unless they should actually be re-sent).
			Emails successfully delivered are marked as 'sent', and those
			that fail to be deliver are marked as 'exception', and the
			corresponding error mail is output in the server logs.

			:param bool auto_commit: whether to force a commit of the mail status
				after sending each mail (meant only for scheduler processing);
				should never be True during normal transactions (default: False)
			:param bool raise_exception: whether to raise an exception if the
				email sending process has failed
			:return: True
		"""
		context = dict(context or {})
		ir_mail_server = self.pool.get('ir.mail_server')
		ir_attachment = self.pool['ir.attachment']
		attachment_ids =[]
		attachments =[]

		for mail in self.browse(cr, SUPERUSER_ID, ids, context=context):
			try:
				# TDE note: remove me when model_id field is present on mail.message - done here to avoid doing it multiple times in the sub method
				if mail.model:
					model_id = \
						self.pool['ir.model'].search(cr, SUPERUSER_ID, [('model', '=', mail.model)], context=context)[0]
					model = self.pool['ir.model'].browse(cr, SUPERUSER_ID, model_id, context=context)
				else:
					model = None
				if model:
					context['model_name'] = model.name

				# load attachment binary data with a separate read(), as prefetching all
				# `datas` (binary field) could bloat the browse cache, triggerring
				# soft/hard mem limits with temporary data.
				#-------------------------Choix du serveur SMTP----------------------
				try:
					mail_server_id = self.pool.get('ir.mail_server').search(cr,uid,[('user_id','=',uid)])[0]

				except:
					mail_server_id = self.pool.get('ir.mail_server').search(cr, uid, [])[0]

				# -------------------------récupération des pièces jointes-------------------
				active_record = self.browse(cr, uid, ids[0], context=context)

				res = self.create_attachments(cr, uid, ids, context=None)

				if res:
					attachment_ids = self.pool.get('ir.attachment').search(cr, uid, [('res_id', "=", active_record.id),
																				('res_model','like',active_record._name)],
																	   context=context)
					attachments = [(a['datas_fname'], base64.b64decode(a['datas']))
								   for a in ir_attachment.read(cr, SUPERUSER_ID, attachment_ids,
															   ['datas_fname', 'datas'])]
				else:
					pass

				# ----------------------------------------------------------------------------
				# specific behavior to customize the send email for notified partners
				email_list = []
				if mail.email_to:
					email_list.append(self.send_get_email_dict(cr, uid, mail, context=context))
				for partner in mail.recipient_ids:
					email_list.append(self.send_get_email_dict(cr, uid, mail, partner=partner, context=context))
				# headers
				headers = {}
				bounce_alias = self.pool['ir.config_parameter'].get_param(cr, uid, "mail.bounce.alias", context=context)
				catchall_domain = self.pool['ir.config_parameter'].get_param(cr, uid, "mail.catchall.domain",
																			 context=context)
				if bounce_alias and catchall_domain:
					if mail.model and mail.res_id:
						headers['Return-Path'] = '%s-%d-%s-%d@%s' % (
							bounce_alias, mail.id, mail.model, mail.res_id, catchall_domain)
					else:
						headers['Return-Path'] = '%s-%d@%s' % (bounce_alias, mail.id, catchall_domain)
				if mail.headers:
					try:
						headers.update(eval(mail.headers))
					except Exception:
						pass

				# Writing on the mail object may fail (e.g. lock on user) which
				# would trigger a rollback *after* actually sending the email.
				# To avoid sending twice the same email, provoke the failure earlier
				mail.write({'state': 'exception'})
				mail_sent = False

				# build an RFC2822 email.message.Message object and send it without queuing
				res = None
				for email in email_list:
					msg = ir_mail_server.build_email(
						email_from=mail.email_from,
						email_to=email.get('email_to'),
						subject=email.get('subject'),
						body=email.get('body'),
						body_alternative=email.get('body_alternative'),
						email_cc=tools.email_split(mail.email_cc),
						#--------envoi en cci
						email_bcc=tools.email_split(mail.email_bcc),
						#-------------------
						reply_to=mail.reply_to,
						attachments=attachments,
						message_id=mail.message_id,
						references=mail.references,
						object_id=mail.res_id and ('%s-%s' % (mail.res_id, mail.model)),
						subtype='html',
						subtype_alternative='plain',
						headers=headers)
					try:
						res = ir_mail_server.send_email(cr, uid, msg,
														mail_server_id=mail_server_id,
														context=context)

					except AssertionError as error:
						self.pool.get('ir.attachment').unlink(cr, uid, attachment_ids, context=None)

						if error.message == ir_mail_server.NO_VALID_RECIPIENT:
							# No valid recipient found for this particular
							# mail item -> ignore error to avoid blocking
							# delivery to next recipients, if any. If this is
							# the only recipient, the mail will show as failed.
							_logger.warning("Ignoring invalid recipients for mail.information %s: %s",
											mail.message_id, email.get('email_to'))
						else:
							raise
				if res:
					mail.write({'state': 'sent', 'message_id': res})
					mail_sent = True

				# /!\ can't use mail.state here, as mail.refresh() will cause an error
				# see revid:odo@openerp.com-20120622152536-42b2s28lvdv3odyr in 6.1
				if mail_sent:
					_logger.info('Mail with ID %r and Message-Id %r successfully sent', mail.id, mail.message_id)
				self._postprocess_sent_message(cr, uid, mail, context=context, mail_sent=mail_sent)
			except MemoryError:
				# prevent catching transient MemoryErrors, bubble up to notify user or abort cron job
				# instead of marking the mail as failed
				_logger.exception('MemoryError while processing mail with ID %r and Msg-Id %r. ' \
								  'Consider raising the --limit-memory-hard startup option',
								  mail.id, mail.message_id)
				raise
			except psycopg2.Error:
				# If an error with the database occurs, chances are that the cursor is unusable.
				# This will lead to an `psycopg2.InternalError` being raised when trying to write
				# `state`, shadowing the original exception and forbid a retry on concurrent
				# update. Let's bubble it.
				raise
			except Exception as e:
				_logger.exception('failed sending mail.information %s', mail.id)
				mail.write({'state': 'exception'})
				self._postprocess_sent_message(cr, uid, mail, context=context, mail_sent=False)
				if raise_exception:
					if isinstance(e, AssertionError):
						# get the args of the original error, wrap into a value and throw a MailDeliveryException
						# that is an except_orm, with name and value as arguments
						value = '. '.join(e.args)
						raise MailDeliveryException(_("Mail Delivery Failed"), value)
					raise

			if auto_commit is True:
				cr.commit()

		return True



############################################classe pour les filtres sur les mails 
class mail_info_filtre(osv.osv_memory):
	""" Model holding RFC2822 email messages to send. This model also provides
		facilities to queue and send new email messages.  """
	_name = 'mail.information.filtre'

	_columns = {
		'filter_type': fields.selection([('product', u'Tous les opérateurs économiques qui ont commandé un produit particulier'), ('etat_adhesion', u'Tous les opérateurs économiques qui ont une adhésion'),('secteur_activite', u'Tous les opérateurs économiques qui appartient à un ou plusieurs secteurs d\'activités'),('group', u'Tous les opérateurs économiques qui appartient à un groupe particulier')], string="Critère"),
		'product_id': fields.many2one('product.template', 'Produit'),
		'etat_adhesion': fields.selection([('membre_payant', u'Membre payant'), ('autre', 'Autre')], u'Etat d\'adhésion'),
		'secteur_activite': fields.many2many('res.partner.category', 'mail_info_filtre_categ_res_partner_rel',
											 'categ_res_partner_id', 'mail_info_filtre_id', u'Secteur d\'activité'),
		'group_id': fields.many2one('res.partner.group', 'Groupe particulier'),
	}


	def onchange_case_product_id(self, cr, uid, ids, product_id):
		res = {}
		lead_ids = self.pool.get('crm.lead').search(cr, uid, [('stage_id', '=', 6)])
		lead_objs = self.pool.get('crm.lead').browse(cr, uid, lead_ids)
		prod_ids = []
		for obj in lead_objs:
			id_prod = obj.product_id.id
			prod_ids.append(id_prod)

		res['domain'] = {'product_id': [('id', 'in', prod_ids)]}
		return res

	def send_info_mail(self, cr, uid, ids, context=None):
		filter_type = self.browse(cr, uid, ids[0], context=context).filter_type
		product_id = self.browse(cr, uid, ids[0], context=context).product_id.id
		etat_adhesion = self.browse(cr, uid, ids[0], context=context).etat_adhesion
		group_id = self.browse(cr, uid, ids[0], context=context).group_id.id
		secteur_activite_ids =[]

		for sec_act_obj in self.browse(cr, uid, ids[0], context=context).secteur_activite:
			secteur_activite_ids.append(sec_act_obj.id)


		new_mail_info = 0

		if filter_type:
			new_mail_info = self.pool.get('mail.information').create(cr, uid,{
				'type_menu':'Adherent'}, context=context)


			if filter_type == 'product':
				if product_id:
					lead_ids = self.pool.get('crm.lead').search(cr, uid, [('stage_id', '=', 6),
																		  ('product_id', '=', product_id)])
					lead_objs = self.pool.get('crm.lead').browse(cr, uid, lead_ids)
				else:
					lead_ids = self.pool.get('crm.lead').search(cr, uid, [('stage_id', '=', 6)])
					lead_objs = self.pool.get('crm.lead').browse(cr, uid, lead_ids)

				op_eco_particip_ids = []
				for obj in lead_objs:
					partner_id = obj.partner_id.id
					op_eco_particip_ids.append(partner_id)


				for op_eco_id in list(set(op_eco_particip_ids)):
					
					cr.execute(
						'INSERT INTO mail_information_res_partner_rel(mail_information_id,res_partner_id) VALUES(' + str(
							new_mail_info) + ',' + str(op_eco_id) + ')')



			elif filter_type == 'etat_adhesion':

				if etat_adhesion == "membre_payant":
					op_eco_ids = self.pool.get('res.partner').search(cr, uid, [('membership_state', '=', 'paid')])
				elif etat_adhesion == "autre":
					op_eco_ids = self.pool.get('res.partner').search(cr, uid, [('membership_state', '!=', 'paid')])
				else:
					op_eco_ids = self.pool.get('res.partner').search(cr, uid, [])

				for op_eco_id in op_eco_ids:
					cr.execute(
						'INSERT INTO mail_information_res_partner_rel(mail_information_id,res_partner_id) VALUES(' + str(
							new_mail_info) + ',' + str(op_eco_id) + ')')


			elif filter_type == 'secteur_activite':
				all_op_eco_ids = []
				if secteur_activite_ids:
					for sec_act_id in secteur_activite_ids:
						cr.execute('SELECT partner_id FROM res_partner_res_partner_category_rel WHERE category_id =' + str(sec_act_id))
						#cr.execute('SELECT r.partner_id FROM res_partner r,res_partner_res_partner_category_rel c WHERE c.category_id =' + str(sec_act_id) + ' AND c.partner_id = r.id AND r.is_company = True ')
						res = cr.fetchall()
						op_eco_ids = [x[0] for x in res]
						all_op_eco_ids.extend(op_eco_ids)
						print '.......',list(set(all_op_eco_ids))
					# list(set(all_op_eco_ids)) contient les opérateurs économiques sans redendance
					for op_eco_id in list(set(all_op_eco_ids)):
						cr.execute('INSERT INTO mail_information_res_partner_rel(mail_information_id,res_partner_id) VALUES(' + str(new_mail_info) + ',' + str(op_eco_id) + ')')

				else:
					cr.execute('SELECT DISTINCT(partner_id) FROM res_partner_res_partner_category_rel')

					res = cr.fetchall()
					op_eco_ids = [x[0] for x in res]
					for op_eco_id in op_eco_ids:
						cr.execute(
							'INSERT INTO mail_information_res_partner_rel(mail_information_id,res_partner_id) VALUES(' + str(
								new_mail_info) + ',' + str(op_eco_id) + ')')
			elif filter_type == 'group':
				print '...............................group'
				if group_id:
					print '........res_partner_group........',group_id
					cr.execute('SELECT partner_id FROM group_partner_rel WHERE group_id =' + str(group_id,))
					res = cr.fetchall()
					print 'resultat :',res
					op_eco_ids = [x[0] for x in res]
					for op_eco_id in op_eco_ids:
						cr.execute('INSERT INTO mail_information_res_partner_rel(mail_information_id,res_partner_id) VALUES(' + str(new_mail_info) + ',' + str(op_eco_id) + ')')

			#update 20-09-2017 by marwa bm
			mail_info = self.pool.get('mail.information').write(cr, uid,new_mail_info,{'subject':'','type_menu':'Adherent'}, context=context)
		else:
			print "veuillez choisir un filtre"

		return {
			'name': "Lettre d'information pour opérateurs économiques",
			'view_type': 'form',
			'view_mode': 'form',
			'view_id ref= view_mail_information_form22': True,
			'res_model': 'mail.information',
			'res_id': int(new_mail_info),
			'type': 'ir.actions.act_window',
			'flags': {'form': {'options': {'mode': 'edit'}}},
		}

