from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from datetime import datetime,timedelta
import calendar

class hr_avance(osv.osv):
    _name = 'hr.avance'
    _inherit = 'mail.thread'
    
    
    def _employee_get(self, cr, uid, context=None):        
        emp_id = context.get('default_employee_id', False)
        if emp_id:
            return emp_id
        ids = self.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)], context=context)
        if ids:
            return ids[0]
        return False

    _columns = {
        'employee_id': fields.many2one('hr.employee', 'Employee', required=True, readonly=True, states={'draft': [('readonly', False)]}),
	'date':fields.date('Date',required=True,readonly=True, states={'draft': [('readonly', False)]}),
        'state': fields.selection([
            ('draft', 'Brouillon'),
            ('sent', 'Envoyée'),
            ('done', 'Acceptée'),
            ('cancel', 'Refusée'),
        ]),
	'montant':fields.float('Montant demandé',required=True,readonly=True, states={'draft': [('readonly', False)]}),
	'description':fields.text('Description',readonly=True, states={'draft': [('readonly', False)]}),
    }
    _defaults = {
	
		'state':'draft',
        'employee_id': _employee_get,
    }

		
		
		
    def create(self,cr, uid, values, context=None):
	res=0
	employee_id = values.get('employee_id', False)
        #demande_avance=self.browse(cr, uid, ids)
	montant = values.get('montant', False)
		
        contract_ids=self.pool.get('hr.contract').search(cr, uid, [('employee_id', '=',employee_id)])
		
        contract = self.pool.get('hr.contract').browse(cr, uid,contract_ids)


    	if montant > contract.wage:

			#raise osv.except_osv(_('Montant erroné'), _('Montant demandé supperieur à votre salaire '))
			raise osv.except_osv(('Montant erroné'), ('Montant demandé supperieur à votre salaire '))
        else :
		res=super(hr_avance, self).create(cr, uid, values, context)
        return res
## il faut redefenir le write aussi !! 

    def envoyer(self, cr, uid, ids, context):
        '''
           Methode du workflow: changer l'état du demande à l'état envoyé
        ''' 
        demande_avance=self.browse(cr, uid, ids)
        montant=0.0
        mois=int(demande_avance.date[5:-3])
        year= datetime.now().year
        from_date=datetime(year,mois,1)
        to_date=datetime(year,mois,calendar.monthrange(year,mois)[1])

        contract_ids=self.pool.get('hr.contract').search(cr, uid, [('employee_id', '=', demande_avance.employee_id.id)])
		
        contract = self.pool.get('hr.contract').browse(cr, uid,contract_ids)
        avance_ids = self.pool.get('hr.avance').search(cr, uid, [('employee_id','=',demande_avance.employee_id.id),('state','not in',['draft']),('date','>=',from_date),('date','<=',to_date)])
        avance_obj = self.pool.get('hr.avance').browse(cr, uid, avance_ids)
        if avance_obj:
        
        
		    if int(contract.type_avance)==1:
		    		raise osv.except_osv(('Deux demandes d\'avance pour un seul mois'), ('Vous avez déjà envoyé une demande d\'avance pour ce mois '))

		    elif int(contract.type_avance)==2:
		    		for avance in avance_obj:
						montant+=avance.montant
						if montant+demande_avance.montant > contract.wage:
							raise osv.except_osv(('Montant erroné'), ('Montant demandé pour ce mois est supperieur à votre salaire '))
							
							
		
		
        #groups=self.pool.get('res.groups').browse(cr, uid,50, context=context)
        name_categ='Human Resources'
        cr.execute('SELECT id FROM ir_module_category WHERE name= %s ', (name_categ,))
        rec=cr.dictfetchone()

        categ_id=rec['id']

        
        name_grp='Manager'
        cr.execute('SELECT id FROM res_groups WHERE name= %s AND category_id=%s ', (name_grp,categ_id,))
        rec=cr.dictfetchone()

        gpg_id=rec['id']
        cr.execute('SELECT id FROM res_users,res_groups_users_rel WHERE res_users.id = res_groups_users_rel.uid AND res_users.active = True AND res_groups_users_rel.gid =%s ', (gpg_id,))
        record=cr.dictfetchall()

        if len(record) > 0:
        	for user in record:
        		user_id=user['id']	
		
        
		    	mail_vals = {

					'body':'<html>Vous avez une demande d\'avance </html>',
					'record_name':'demande',
					'res_id':ids[0],
					'reply_to':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
					'author_id':self.pool.get('res.users').browse(cr, uid, uid, context=context).partner_id.id,
					'model':'hr.avance',
					'type':'comment',
					'email_from':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
					'starred':True,
				}
			
		    	message = self.pool.get('mail.message').create(cr, uid, mail_vals) 		
			
		    	mail_notif_vals = {		
			
			

			
			
					'partner_id':self.pool.get('res.users').browse(cr, uid,user_id, context=context).partner_id.id,
					'message_id':message,
					'is_read':False,
					'starred':True,
				
				}
		    	self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)
			
			

		self.write(cr, uid, ids, {'state': 'sent'})
		return True
		 
		    

    def confirmer(self, cr, uid, ids, context):
        '''
           Methode du workflow: changer l'état du demande à l'état accepté
        ''' 
        demande_avance=self.browse(cr, uid, ids)

	mail_vals = {
		'body':'<html>Votre demande d\'avance a été acceptée</html>',
		'record_name':'Demande acceptée',
		'res_id':ids[0],
		'reply_to':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
		'author_id':self.pool.get('res.users').browse(cr, uid, uid, context=context).partner_id.id,
		'model':'hr.avance',
		'type':'comment',
		'email_from':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
		'starred':True,
	}
	message = self.pool.get('mail.message').create(cr, uid, mail_vals) 

			
	mail_notif_vals = {
		'partner_id':self.pool.get('res.users').browse(cr, uid,demande_avance.employee_id.user_id.id, context=context).partner_id.id,
		'message_id':message,
		'is_read':False,
		'starred':True,
				
	}
	self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)

        self.write(cr, uid, ids, {'state': 'done'})
        return True

    def refuser(self, cr, uid, ids, context):
        '''
           Methode du workflow: changer l'état du demande à l'état refusé
        ''' 
        demande_avance=self.browse(cr, uid, ids)
	mail_vals = {
		'body':'<html>Votre demande d\'avance a été refusée</html>',
		'record_name':'Demande refusée',
		'res_id':ids[0],
		'reply_to':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
		'author_id':self.pool.get('res.users').browse(cr, uid, uid, context=context).partner_id.id,
		'model':'hr.avance',
		'type':'comment',
		'email_from':self.pool.get('res.users').browse(cr, uid, uid, context=context).name,
		'starred':True,
	}
	message = self.pool.get('mail.message').create(cr, uid, mail_vals) 

			
	mail_notif_vals = {
		'partner_id':self.pool.get('res.users').browse(cr, uid,demande_avance.employee_id.user_id.id, context=context).partner_id.id,
		'message_id':message,
		'is_read':False,
		'starred':True,
				
	}
	self.pool.get('mail.notification').create(cr, uid, mail_notif_vals)
        self.write(cr, uid, ids, {'state': 'cancel'})
        return True
hr_avance()


class hr_contract(osv.osv):
    _inherit = 'hr.contract'

    _columns = {
        'type_avance': fields.selection([('1', 'Une fois/mois'),('2','Suiant salaire')], 'Plafond Avance', required=True, ),
    }
hr_contract()



























