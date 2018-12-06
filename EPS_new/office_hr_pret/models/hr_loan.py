#-*- coding:utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import except_orm, Warning, RedirectWarning
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar


class hr_loan(models.Model):
	_name = 'hr.loan'
	_inherit = ['mail.thread','ir.needaction_mixin']
	_description= "Demande pret"

	@api.one
	@api.depends('taux', 'loan_amount')
	def _amount_total_loan(self):
		self.total_loan_amount = self.loan_amount+(self.loan_amount*self.taux/100)

	@api.one
	@api.depends('taux_plafond','emp_salary')
	def _amount_plafond_payement(self):
		print "self.taux_plafond=====",self.taux_plafond
		self.plafond_payement = (self.emp_salary * self.taux_plafond)/100
		print "self.plafond_payement=========",self.plafond_payement

	name = fields.Char(string="Référence", default="/", readonly=True)
	date = fields.Date(string="Date du Demande", default=fields.Date.today(), readonly=True)
	employee_id = fields.Many2one('hr.employee', string="Employee", required=True, readonly=True, states={'draft': [('readonly', False)]})
	emp_salary = fields.Float(string="Salaire Employee",related="employee_id.contract_id.wage", readonly=True)
	#type_pret= fields.Selection([('1', 'Societe'),('2','CNSS'),('3','Banque')], 'Type Pret', required=True, )
	#motif_pret= fields.Many2one('hr.loan.motif', 'Motif Pret', required=True, )
	#taux = fields.Float(string="Taux Intéret %", default=0.0)
	taux_plafond = fields.Float(string="Taux Plafond payement %", required=True,default=100.0,readonly=True, states={'draft': [('readonly', False)]})
	plafond_payement = fields.Float(string="Plafond Payement mensuel", readonly=True,compute='_amount_plafond_payement')
	plafond = fields.Float(string="Plafond Pret",default=30, required=True)
	loan_amount = fields.Float(string="Montant", required=True,readonly=True, states={'draft': [('readonly', False)]})
	#total_loan_amount = fields.Float(string="Montant Total", readonly=True,compute='_amount_total_loan')
	no_month = fields.Integer(string="Nombre des mois", default=1,readonly=True, states={'draft': [('readonly', False)]})

	#champs ajoutés
	mnt_paye = fields.Float(string="Montant paye", readonly=True)
	reste = fields.Float(string="Reste à payer", compute='calcul_reste')

	loan_line_ids = fields.One2many('hr.loan.line', 'loan_id', string="Loan Line", index=True)
	payment_start_date = fields.Date(string="Date Début du Paiement", required=True,readonly=True, states={'draft': [('readonly', False)]})
	state = fields.Selection([
		('draft','Brouillon'),
		('approve','Approuvée'),
		('refuse','Refusée'),
		('cloture','Cloturée'),
	], string="State", default='draft', track_visibility='onchange', copy=False,)
	
		
	#code ajoute pour calculer le reste à payer
	def calcul_reste(self):
		self.reste=self.loan_amount-self.mnt_paye
		print 'reste=============',self.reste


	#code pour changer le status et la date de paiement 
	@api.onchange('loan_line_ids') # if these fields are changed, call method
	def check_change(self):
		employee_id = self.employee_id.id

		if employee_id != False :

			counter = 1
			for loan in self:
				loan_line = self.loan_line_ids
				tot = 0
				for line in loan_line:
					if line.state == '1':
						tot = tot + line.paid_amount
						i=line.id

				date_start = self.env['hr.loan.line'].browse(i).paid_date
				date_start_str = datetime.strptime(date_start ,'%Y-%m-%d')


				for line in loan_line:
					if line.state == '2':
						date_start_str = date_start_str + relativedelta(months = 1)
						self.env.cr.execute('UPDATE hr_loan_line SET paid_date=%s WHERE id=%s',(date_start_str,line.id))
				self.env.cr.execute('UPDATE hr_loan SET mnt_paye=%s WHERE employee_id=%s',(tot,employee_id))







	@api.multi
	def reglement_total(self):
		print "hello"
		loan_line = self.env['hr.loan.line']

		self.mnt_paye = self.loan_amount
		print "mnt paye====",self.mnt_paye

		self.reste=self.mnt_paye-self.reste
		print "reste=======",self.reste

		print "employee_id",self.employee_id.id

		for loan in self:
			print "line",loan_line
			#line_id = loan_line.write({'state':'1'})
			self.env.cr.execute('UPDATE hr_loan_line SET state=%s WHERE employee_id=%s',('1',self.employee_id.id))
			print 'i do it'
		self.state = 'cloture'

	@api.model
	def create(self, values):
		values['name'] = self.env['ir.sequence'].get('hr.loan.req') or ' '
		res = super(hr_loan, self).create(values)
		return res

	@api.one
	def action_refuse(self):
		self.state = 'refuse'
		
		
	@api.one
	def action_set_to_draft(self):
		self.state = 'draft'

	@api.multi
	def compute_loan_line(self):

		loan_line = self.env['hr.loan.line']
		loan_line.search([('loan_id','=',self.id)]).unlink()
		for loan in self:
			date_start_str = datetime.strptime(loan.payment_start_date,'%Y-%m-%d')
			counter = 1
			
			amount_per_time = loan.loan_amount / loan.no_month
			contract = self.env['hr.contract']
			contract_ids=contract.search([('employee_id','=',loan.employee_id.id)])
			wage=0.0
			for cont in contract_ids:
				wage+=cont.wage

			if amount_per_time > loan.plafond_payement:
				raise except_orm('Warning', 'Montant du tranche est supérieur au plafond mensuel du pret')
			for i in range(1, loan.no_month + 1):
				
				mois=int(str(date_start_str)[5:-12])
				year=int(str(date_start_str)[:-15])
				from_date=datetime(year,mois,1)
				to_date=datetime(year,mois,calendar.monthrange(year,mois)[1])
				loan_line_credit=loan_line.search([('paid_date','>=',from_date),('paid_date','<=',to_date),('employee_id','=',loan.employee_id.id)])#,('loan_id.state','in',['approve'])
				credit_amount=0.0
				for credit in loan_line_credit:
					credit_amount+=credit.paid_amount

				total_payement=amount_per_time+credit_amount
				if total_payement > loan.plafond_payement:
					raise except_orm('Warning', 'Vous avez déjà un payement dans la periode du '+str(from_date)[:-8]+' Au '+str(to_date)[:-8])
				line_id = loan_line.create({
					'paid_date':date_start_str, 
					'paid_amount': amount_per_time,
					'employee_id': loan.employee_id.id,
					'loan_id':loan.id})
				counter += 1
				date_start_str = date_start_str + relativedelta(months = 1)
				
		return True


	@api.one
	def action_approve(self):
		self.state = 'approve'
		if not self.loan_line_ids:
			raise except_orm("Warning", "Vous devez calculer les tranches du pret avant l'approvée")
		
		return True

	@api.one
	def action_cloture(self):
		if self.loan_amount == self.mnt_paye :
			print"yessssss i do it "
			self.state = 'cloture'
		else:
			self.state = 'approve'
			print "nooooooo not yet"
		return True

			
		
	

class hr_loan_line(models.Model):
	_name="hr.loan.line"
	_description = "Ligne du demande de pret "


	paid_date = fields.Date(string="Date Paiement", required=True)
	employee_id = fields.Many2one('hr.employee', string="Employee",readonly=True)
	loan_id =fields.Many2one('hr.loan', string="Ref Pret", ondelete='cascade',readonly=True)
	paid_amount= fields.Float(string="Montant", required=True,readonly=True)
	# exemple 'note_line_id': fields.one2many('note','cmd_id',"Note lines"),
	#wzd_mois=fields.One2many('wizard.regler.mensualite','mois')
	#code ajouté 
	state = fields.Selection([
		('1','Deduite'),
		('2','Non deduite'),
	], string="Status", default='2',)



class hr_loan_motif(models.Model):
	_name="hr.loan.motif"
	_description = "Les Motif des prets"



	name = fields.Char(string="Nom",  required=True)
	
	
	
	
	
	
	
	
	
	
	
	
