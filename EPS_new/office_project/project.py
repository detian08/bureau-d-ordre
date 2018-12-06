# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime, date
from lxml import etree
import time
from operator import eq
from openerp import SUPERUSER_ID, api
from openerp import tools
from openerp.addons.resource.faces import task as Task
from openerp.osv import fields, osv
from openerp.tools import float_is_zero
from openerp.tools.translate import _


class task(osv.osv):
    _name = "project.task"

    _inherit = 'project.task'
    
    def _visibility_button(self, cr, uid, ids, field_name, arg, context): 
	
		res = {}
		for tache in self.browse(cr, uid, ids, context=context):

		    res[tache.id] = False
		    if tache.user_id.id==uid:
		    	res[tache.id] = True

		return  res

    _columns = {
		'stage_id': fields.many2one('project.task.type', 'Stage',  select=True,
                        domain="[('project_ids', '=', project_id)]", copy=False),
        
		'visibility_button':fields.function(_visibility_button, type="boolean", method=True),
		'name': fields.char('Task Summary', track_visibility='onchange', size=128, required=True, select=True,readonly=True,states={'draft':[('readonly',False)]}),
		'user_id': fields.many2one('res.users', 'Assigned to', select=True, track_visibility='onchange',readonly=True,states={'draft':[('readonly',False)]}),
		'date_deadline': fields.date('Deadline', select=True, copy=False,readonly=True,states={'draft':[('readonly',False)]}),
		'partner_id': fields.many2one('res.partner', 'Customer',readonly=True,states={'draft':[('readonly',False)]}),
		'categ_ids': fields.many2many('project.category', string='Tags',readonly=True,states={'draft':[('readonly',False)]}),            
		'user_cc_ids': fields.many2many('res.users',string="Employés en copie"),
		'group_gerant_id': fields.many2one('res.groups', ),
		'state': fields.selection([('draft', 'Brouillon'),
                                   ('sent', 'Envoyée'),
                                   ('waiting', 'En cours de preparation'),
                                   ('done', 'Terminé'),
                                   ], 'Status', readonly=True, select=True, copy=False,
                ),





    }
    
    
    _defaults = {
    	'state': 'draft',
    	'group_gerant_id':lambda self, cr, uid, ctx=None: self.pool.get('res.groups').search(cr, uid, [('name','=','Gérant')], context=ctx)[0]
    
    }
    
    
    
    
    
    def action_sent(self, cr, uid, ids, context=None):
		for tache in self.browse(cr, uid, ids, context=context):
			mail_vals = {
					'body':'<html>Vous avez une nouvelle tache à réaliser </html>',
					'record_name':tache.name,
					'res_id':tache.id,
					'reply_to':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
					'author_id':self.pool.get('res.users').browse(cr, uid, uid, context=context).partner_id.id,
					'model':'project.task',
					'type':'comment',
					'email_from':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
					'starred':True,
			}
			message = self.pool.get('mail.message').create(cr, uid, mail_vals)
			mail_notif_vals = {				

					'partner_id':self.pool.get('res.users').browse(cr, uid,tache.user_id.id, context=context).partner_id.id,
					'message_id':message,
					'is_read':False,
					'starred':True,
			}								
			self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)
    		
			mail_vals_copie = {
					'body':'<html>Une nouvelle tache assignée à '+tache.user_id.name.encode('UTF-8')+' </html>',
					'record_name':tache.name,
					'res_id':tache.id,
					'reply_to':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
					'author_id':self.pool.get('res.users').browse(cr, uid, uid, context=context).partner_id.id,
					'model':'project.task',
					'type':'comment',
					'email_from':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
					'starred':True,
			}
			message = self.pool.get('mail.message').create(cr, uid, mail_vals_copie)
			users_en_copie=[user.id for user in tache.user_cc_ids ]
			for user in users_en_copie:
				mail_notif_vals_copie = {				

						'partner_id':self.pool.get('res.users').browse(cr, uid,user, context=context).partner_id.id,
						'message_id':message,
						'is_read':False,
						'starred':True,
				}								
				self.pool.get('mail.notification').create(cr, uid, mail_notif_vals_copie)
    		
		task_type_ids=self.pool.get('project.task.type').search(cr, uid, [('name', '=', 'Envoyer')])
		taks_type=self.pool.get('project.task.type').browse(cr, uid, task_type_ids)
								

		self.write(cr, uid, ids, {'state': 'sent','stage_id':taks_type.id}, context=context)
		return True
    	
    def action_accept(self, cr, uid, ids, context=None):
    	for tache in self.browse(cr, uid, ids, context=context):
    		mail_vals = {
					'body':'<html> Tache en cours de préparation </html>',
					'record_name':tache.name,
					'res_id':tache.id,
					'reply_to':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
					'author_id':self.pool.get('res.users').browse(cr, uid, uid, context=context).partner_id.id,
					'model':'project.task',
					'type':'comment',
					'email_from':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
					'starred':True,
			}
    		message = self.pool.get('mail.message').create(cr, uid, mail_vals)
    		mail_notif_vals = {				
			
					'partner_id':self.pool.get('res.users').browse(cr, uid,tache.reviewer_id.id, context=context).partner_id.id,
					'message_id':message,
					'is_read':False,
					'starred':True,
    		}								
    		self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)
    		mail_vals_copie = {
					'body':'<html> '+tache.user_id.name.encode('UTF-8')+' est en cours de préparer la tache </html>',
					'record_name':tache.name,
					'res_id':tache.id,
					'reply_to':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
					'author_id':self.pool.get('res.users').browse(cr, uid, uid, context=context).partner_id.id,
					'model':'project.task',
					'type':'comment',
					'email_from':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
					'starred':True,
			}
    		message = self.pool.get('mail.message').create(cr, uid, mail_vals_copie)
    		users_en_copie=[user.id for user in tache.user_cc_ids ]
    		for user in users_en_copie:
				mail_notif_vals_copie = {				
			
						'partner_id':self.pool.get('res.users').browse(cr, uid,user, context=context).partner_id.id,
						'message_id':message,
						'is_read':False,
						'starred':True,
				}								
				self.pool.get('mail.notification').create(cr, uid, mail_notif_vals_copie)		
    	task_type_ids=self.pool.get('project.task.type').search(cr, uid, [('name', '=', 'En cours de preparation')])
    	taks_type=self.pool.get('project.task.type').browse(cr, uid, task_type_ids)
    
    	self.write(cr, uid, ids, {'state': 'waiting','stage_id':taks_type.id}, context=context)	
    	return True
    
    def action_done(self, cr, uid, ids, context=None):
    	for tache in self.browse(cr, uid, ids, context=context):
    		mail_vals = {
					'body':'<html> Tache Terminé </html>',
					'record_name':tache.name,
					'res_id':tache.id,
					'reply_to':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
					'author_id':self.pool.get('res.users').browse(cr, uid, uid, context=context).partner_id.id,
					'model':'project.task',
					'type':'comment',
					'email_from':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
					'starred':True,
			}
    		message = self.pool.get('mail.message').create(cr, uid, mail_vals)
    		mail_notif_vals = {				
			
					'partner_id':self.pool.get('res.users').browse(cr, uid,tache.reviewer_id.id, context=context).partner_id.id,
					'message_id':message,
					'is_read':False,
					'starred':True,
    		}								
    		self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)
    		
    	task_type_ids=self.pool.get('project.task.type').search(cr, uid, [('name', '=', 'Done')])
    	taks_type=self.pool.get('project.task.type').browse(cr, uid, task_type_ids)
    	self.write(cr, uid, ids, {'state': 'done','stage_id':taks_type.id}, context=context)	
    	return True
    	
    	
    
    
    
    
    
    

	












