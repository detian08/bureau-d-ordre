# -*- coding: utf-8 -*-
from datetime import date, datetime
from dateutil import relativedelta
from openerp import tools
from openerp import api
from openerp.osv import fields, osv
from datetime import datetime
from openerp.tools.translate import _
from openerp.exceptions import Warning
import openerp

class calendar_attendee_partner(osv.Model):
	_name='calendar.attendee.partner'
	_columns = {
		'attendee_partner_ids': fields.many2many('res.users'),
	}
	def add_attendee_calendar(self,cr, uid, ids, context):
		partner_ids = context.get('partner_ids')[0][2]
		active_id = context.get('active_id')
		for partner in partner_ids:
			partner_id = self.pool.get('res.users').browse(cr,uid,partner,context).partner_id.id
			cr.execute("INSERT INTO calendar_event_res_partner_rel (calendar_event_id, res_partner_id) VALUES (%s, %s)", (active_id,partner_id))

			#self.pool.get('calendar.event').write(cr,uid,active_id,)
		# ret = [self.pool['res.users'].browse(cr, uid, uid, context=ctx).partner_id.id]
		# active_id = ctx.get('active_id')
		# if ctx.get('active_model') == 'res.partner' and active_id:
		# 	if active_id not in ret:
		# 		ret.append(active_id)
		# return ret
		return True

class calendar_event(osv.Model):
	_inherit = "calendar.event"
	_name = 'calendar.event'

	def get_coach_id(self, cr, uid, ids,context=None):
		coach_id=self.pool.get('hr.employee').browse(cr,uid,ids,context=context).coach_id
		return coach_id

	_columns = {
		# 'name': fields.char('Meeting Subject', required=True, states={'done': [('readonly', True)]}),
	'opportunity_ids': fields.many2one('crm.lead','Opportunité'),
	'partner_contact_id':fields.many2many('res.partner','calendar_contact_rel','calendar_event_id','contact_id' ,string="Contacts"),
	'coach_id':fields.integer(),
	}
	_default = {'coach_id':get_coach_id,'partner_ids': lambda self, cr, uid, context: context.get('partner_ids', False),}

	def create(self, cr, uid, vals, context=None):
		name=vals['name']

		if 'opportunity_ids' in vals:
			start_datetime=vals['start_datetime']
			stop_datetime=vals['stop_datetime']
			opportunity_ids=vals['opportunity_ids']
			partner_id=vals['partner_ids'][0][2][0]

			val = {
				'name':name,
				'partner_id':partner_id,
				'date_deadline': stop_datetime,
				'date_action':start_datetime,
				'type':'Reunion',
				'opportunity_ids':opportunity_ids,
				}
			inv_id = self.pool.get('crm.lead.activity').create(cr, uid, val,context=context)
			super(calendar_event, self).create(cr, uid, vals, context=context)
			#rendre les champs vides 22-09-2017
			return self.pool.get('crm.lead').write(cr, uid, opportunity_ids, {'date_deadline': False,'date_action': False,'title_action': False,'type_act': False})
		else :
			return super(calendar_event, self).create(cr, uid, vals, context=context)







	def create_attendees(self, cr, uid, ids, context=None):
		return False

	def closed_action_calendar(self, cr, uid, ids,context=None):
		calendar_id=self.browse(cr, uid, ids,context=context).id
		opportunity_ids=self.browse(cr, uid, ids,context=context).opportunity_ids.id

		return self.pool.get('crm.lead').write(cr, uid, opportunity_ids, {'date_deadline': False,'date_action': False,'title_action': False,'type_act': False})

	def add_attendee(self,cr, uid, ids, context=None):
		return {

			'name': ('Participants'),
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'calendar.attendee.partner',
			'type': 'ir.actions.act_window',
			'view_id ref= view_calendar_attendee_form': True,
			'target': 'new',
		}




