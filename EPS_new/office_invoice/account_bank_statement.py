# -*- coding: utf-8 -*-




from openerp.osv import fields, osv
from openerp.tools import float_is_zero
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.report import report_sxw
from openerp.tools import float_compare, float_round

import time

class account_bank_statement(osv.osv):


	_inherit = 'account.bank.statement'
	
	
	def _get_sum_entry_encoding(self, cr, uid, ids, name, arg, context=None):
		res = {}
		for statement in self.browse(cr, uid, ids, context=context):
			res[statement.id] = sum((line.amount for line in statement.line_ids), 0.0)
			
		return res
		

	def _get_statement_from_line(self, cr, uid, ids, context=None):
		result = {}
		for line in self.pool.get('account.bank.statement.line').browse(cr, uid, ids, context=context):
			result[line.statement_id.id] = True
		return result.keys()
	
	def _end_balance(self, cursor, user, ids, name, attr, context=None):
		res = {}
		for statement in self.browse(cursor, user, ids, context=context):
			res[statement.id] = statement.balance_start
			for line in statement.line_ids:
				res[statement.id] += line.amount
		return res     
     
 
     	
        
	def _get_statement(self, cr, uid, ids, context=None):
		result = {}
		for line in self.pool.get('account.bank.statement.line').browse(cr, uid, ids, context=context):
			result[line.statement_id.id] = True
		return result.keys()
		
		
	def _compute_difference(self, cr, uid, ids, fieldnames, args, context=None):
		result =  dict.fromkeys(ids, 0.0)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = obj.balance_end_real - obj.balance_end
		return result
        

	
	_columns = {
		'total_entry_encoding': fields.function(_get_sum_entry_encoding, string="Total Transactions",digits_compute=dp.get_precision('Account'),store = {'account.bank.statement': (lambda self, cr, uid, ids, context=None: ids, ['line_ids','move_line_ids'], 10),'account.bank.statement.line': (_get_statement_from_line, ['amount'], 10),},help="Total of cash transaction lines."),
		
		'balance_end': fields.function(_end_balance, digits_compute=dp.get_precision('Account'),store = {'account.bank.statement': (lambda self, cr, uid, ids, c={}: ids, ['line_ids','move_line_ids','balance_start'], 10),'account.bank.statement.line': (_get_statement, ['amount'], 10),},string="Computed Balance", help='Balance as calculated based on Opening Balance and transaction lines'),
		
		'difference' : fields.function(_compute_difference, method=True,digits_compute=dp.get_precision('Account'), string="Difference", type="float", help="Difference between the theoretical closing balance and the real closing balance."),
        
            
       
       
	
	
	
	
	
	}
