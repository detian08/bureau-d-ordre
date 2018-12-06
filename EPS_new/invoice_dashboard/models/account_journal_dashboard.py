#-*- coding:utf-8 -*-
import json
from datetime import datetime, timedelta
import calendar
from babel.dates import format_datetime, format_date

from openerp import models, api, _, fields
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.depends('debit', 'credit')
    def _store_balance(self):
        for line in self:
            line.balance = line.debit - line.credit

    balance = fields.Float(compute='_store_balance', store=True, currency_field='company_currency_id', default=0.0, help="Technical field holding the debit - credit in order to open meaningful graph views from reports")


class account_journal(models.Model):
    _inherit = "account.journal"

    @api.one
    def _kanban_dashboard(self):
        self.kanban_dashboard = json.dumps(self.get_journal_dashboard_datas())

    @api.one
    def _kanban_dashboard_graph(self):
        if (self.type in ['sale', 'purchase']):
            self.kanban_dashboard_graph = json.dumps(self.get_bar_graph_datas())
        elif (self.type in ['cash', 'bank']):
            self.kanban_dashboard_graph = json.dumps(self.get_line_graph_datas())

    kanban_dashboard = fields.Text(compute='_kanban_dashboard')
    kanban_dashboard_graph = fields.Text(compute='_kanban_dashboard_graph')
    show_on_dashboard = fields.Boolean(string='Show journal on dashboard', help="Whether this journal should be displayed on the dashboard or not", default=True)

    @api.multi
    def toggle_favorite(self):
        self.write({'show_on_dashboard': False if self.show_on_dashboard else True})
        return False

    @api.multi
    def get_line_graph_datas(self):
        data = []
        today = datetime.today()
        last_month = today + timedelta(days=-30)
        bank_stmt = []
        # Query to optimize loading of data for bank statement graphs
        # Return a list containing the latest bank statement balance per day for the
        # last 30 days for current journal
        query = """SELECT a.date, a.balance_end 
                        FROM account_bank_statement AS a, 
                            (SELECT c.date, max(c.id) AS stmt_id 
                                FROM account_bank_statement AS c 
                                WHERE c.journal_id = %s 
                                    AND c.date > %s 
                                    AND c.date <= %s 
                                    GROUP BY date, id 
                                    ORDER BY date, id) AS b 
                        WHERE a.id = b.stmt_id;"""

        self.env.cr.execute(query, (self.id, last_month, today))
        bank_stmt = self.env.cr.dictfetchall()

        last_bank_stmt = self.env['account.bank.statement'].search([('journal_id', 'in', self.ids),('date', '<=', last_month.strftime(DF))], order="date desc, id desc", limit=1)
        start_balance = last_bank_stmt and last_bank_stmt[0].balance_end or 0

        locale = self._context.get('lang', 'en_US')
        show_date = last_month
        #get date in locale format
        name = format_date(show_date, 'd LLLL Y', locale=locale)
        short_name = format_date(show_date, 'd MMM', locale=locale)
        data.append({'x':short_name,'y':start_balance, 'name':name})

        for stmt in bank_stmt:
            #fill the gap between last data and the new one
            number_day_to_add = (datetime.strptime(stmt.get('date'), DF) - show_date).days
            last_balance = data[len(data) - 1]['y']
            for day in range(0,number_day_to_add + 1):
                show_date = show_date + timedelta(days=1)
                #get date in locale format
                name = format_date(show_date, 'd LLLL Y', locale=locale)
                short_name = format_date(show_date, 'd MMM', locale=locale)
                data.append({'x': short_name, 'y':last_balance, 'name': name})
            #add new stmt value
            data[len(data) - 1]['y'] = stmt.get('balance_end')

        #continue the graph if the last statement isn't today
        if show_date != today:
            number_day_to_add = (today - show_date).days
            last_balance = data[len(data) - 1]['y']
            for day in range(0,number_day_to_add):
                show_date = show_date + timedelta(days=1)
                #get date in locale format
                name = format_date(show_date, 'd LLLL Y', locale=locale)
                short_name = format_date(show_date, 'd MMM', locale=locale)
                data.append({'x': short_name, 'y':last_balance, 'name': name})

        return [{'values': data, 'area': True, 'id': self.id}]

    @api.multi
    def get_bar_graph_datas(self):
        data = []
        year= datetime.now().year
        month=datetime.now().month
        nom_mois_actuel=format_date(datetime(year,month,2), 'MMM', locale=self._context.get('lang', 'en_US'))
        mois_prec=month-1
        print "x===============", month
	print "x111===============", mois_prec
	if mois_prec==0:
	    mois_prec = 12
	    year = year-1

	nom_mois_avant=format_date(datetime(year,mois_prec,2), 'MMM', locale=self._context.get('lang', 'en_US'))
        #mois_prec_prec=month-2
	mois_prec_prec=mois_prec-1
	if mois_prec_prec==0:
	    mois_prec_prec = 12
	    year = year-1
        nom_mois_av_av=format_date(datetime(year,mois_prec_prec,2), 'MMM', locale=self._context.get('lang', 'en_US'))
        today = datetime.strptime(fields.Date.context_today(self), DF)
        data.append({'label': _('Précédent'), 'value':0.0, 'type': 'past'})
        day_of_week = int(format_datetime(today, 'e', locale=self._context.get('lang', 'en_US')))
        first_day_of_week = today + timedelta(days=-day_of_week+1)
        for i in range(-1,2):
            if i==0:
                label = _('Mois du '+nom_mois_avant)
            elif i==1:
                label = _('Mois du '+nom_mois_actuel)
            else :
            	label = _('Mois du '+nom_mois_av_av)
            	            
            #else:
                #start_week = first_day_of_week + timedelta(days=i*7)
                #end_week = start_week + timedelta(days=6)
                #if start_week.month == end_week.month:
                    #label = str(start_week.day) + '-' +str(end_week.day)+ ' ' + format_date(end_week, 'MMM', locale=self._context.get('lang', 'en_US'))
                #else:
                    #label = format_date(start_week, 'd MMM', locale=self._context.get('lang', 'en_US'))+'-'+format_date(end_week, 'd MMM', locale=self._context.get('lang', 'en_US'))
            data.append({'label':label,'value':0.0, 'type': 'past' if i<0 else 'future'})

        # Build SQL query to find amount aggregated by week
        select_sql_clause = """SELECT sum(amount_total) as total, min(date_invoice) as aggr_date from account_invoice where journal_id = %(journal_id)s and state IN ('open','paid')"""
        query = ''
        #start_date = (first_day_of_week + timedelta(days=-7))
        
        #print "start_date=======",start_date
        #print "first_day_of_week===",first_day_of_week
        #print "new_date",new_date
        for i in range(0,4):
	    x= month-3+i
	    print"i=============", i
	    print "x====", x
	    if month==1:
	    	if i==0:
	    	    x=10
		    y = year-1
	            from_date=datetime(y,x,1)
	            to_date = datetime(y,x,calendar.monthrange(y,x)[1])
	    	if i==1:
		    x=11
		    y = year-1
	            from_date=datetime(y,x,1)
	            to_date = datetime(y,x,calendar.monthrange(y,x)[1])
	    	if i==2:
		    x=12
		    y = year
	            from_date=datetime(y,x,1)
	            to_date = datetime(y,x,calendar.monthrange(y,x)[1])
	    	if i==3:
		    print "finnnnnnnnnnnnnn*****"
	            from_date=datetime(year,month-3+i,1)
	            to_date = datetime(year,month-3+i,calendar.monthrange(year,month-3+i)[1])
	    
	    if month==2:
	    	if i==0:
	    	    x=11
		    y = year-1
	            from_date=datetime(y,x,1)
	            to_date = datetime(y,x,calendar.monthrange(y,x)[1])
	    	if i==1:
		    x=12
		    y = year-1
	            from_date=datetime(y,x,1)
	            to_date = datetime(y,x,calendar.monthrange(y,x)[1])
	    	if i>1:
	            from_date=datetime(year,month-3+i,1)
	            to_date = datetime(year,month-3+i,calendar.monthrange(year,month-3+i)[1])

	    if month==3:
	    	if i==0:
	    	    x=12
		    y = year-1
	            from_date=datetime(y,x,1)
	            to_date = datetime(y,x,calendar.monthrange(y,x)[1])
	    	if i>0:
	            from_date=datetime(year,month-3+i,1)
	            to_date = datetime(year,month-3+i,calendar.monthrange(year,month-3+i)[1])
	    if month>3:
            	from_date=datetime(year,month-3+i,1)
            	to_date = datetime(year,month-3+i,calendar.monthrange(year,month-3+i)[1])

            #to_date = datetime(year,month-3+i,calendar.monthrange(year,month-3+i)[1])
            #apres=from_date+ timedelta(month=-1)
            #print "apres=====",apres
            if i == 0:
                query += "("+select_sql_clause+" and date_invoice <= '"+to_date.strftime(DF)+"')"
            elif i == 6:
                query += " UNION ALL ("+select_sql_clause+" and date_invoice >= '"+start_date.strftime(DF)+"')"
            else:
                #next_date = start_date + timedelta(days=7)
                query += " UNION ALL ("+select_sql_clause+" and date_invoice >= '"+from_date.strftime(DF)+"' and date_invoice <= '"+to_date.strftime(DF)+"')"
                #start_date = next_date

        self.env.cr.execute(query, {'journal_id':self.id})
        query_results = self.env.cr.dictfetchall()
        for index in range(0, len(query_results)):
            if query_results[index].get('aggr_date') != None:
                data[index]['value'] = query_results[index].get('total')

        return [{'values': data, 'id': self.id}]

    @api.multi
    def get_journal_dashboard_datas(self):
        currency = self.currency.id or self.company_id.currency_id
        cur_obj = self.pool.get('res.currency')   

        number_to_reconcile = last_balance = account_sum =stock= 0
        ac_bnk_stmt = []
        title = ''
        number_draft = number_waiting = number_late = sum_draft = sum_waiting = sum_late = 0
        if self.type in ['bank', 'cash']:
            last_bank_stmt = self.env['account.bank.statement'].search([('journal_id', 'in', self.ids)], order="date desc, id desc", limit=1)
            #last_balance = last_bank_stmt and last_bank_stmt[0].balance_end or 0
            ac_bnk_stmt = self.env['account.bank.statement'].search([('journal_id', 'in', self.ids),('state', '=', 'open')])

            for ac_bnk in ac_bnk_stmt:
                for line in ac_bnk.line_ids:
                    if not line.journal_entry_id:
                        number_to_reconcile += 1
                last_balance+= ac_bnk.balance_end

            # optimization to read sum of balance from account_move_line
            account_ids = tuple(filter(None, [self.default_debit_account_id.id, self.default_credit_account_id.id]))
            if account_ids:
                query = """SELECT sum(balance) FROM account_move_line WHERE account_id in %s;"""
                self.env.cr.execute(query, (account_ids,))
                query_results = self.env.cr.dictfetchall()
                if query_results and query_results[0].get('sum') != None:
                    account_sum = query_results[0].get('sum')
        #TODO need to check if all invoices are in the same currency than the journal!!!!
        elif self.type in ['sale', 'purchase']:
            title = _('Bills to pay') if self.type == 'purchase' else _('Invoices owed to you')
            # optimization to find total and sum of invoice that are in draft, open state
            query = """SELECT state, amount_total, currency_id AS currency FROM account_invoice WHERE journal_id = %s AND state NOT IN ('paid', 'cancel');"""
            self.env.cr.execute(query, (self.id,))
            query_results = self.env.cr.dictfetchall()
            today = datetime.today()
            query = """SELECT amount_total, currency_id AS currency FROM account_invoice WHERE journal_id = %s AND date_invoice < %s AND state = 'open';"""
            self.env.cr.execute(query, (self.id, today))
            late_query_results = self.env.cr.dictfetchall()
            sum_draft = 0.0
            number_draft = 0
            number_waiting = 0
            for result in query_results:
                cur = self.env['res.currency'].browse(result.get('currency'))
                if result.get('state') in ['draft', 'proforma', 'proforma2']:
                    number_draft += 1
                    sum_draft += cur.compute(result.get('amount_total'), currency)
                elif result.get('state') == 'open':
                    number_waiting += 1
                    sum_waiting += cur.compute(result.get('amount_total'), currency)
            sum_late = 0.0
            number_late = 0
            for result in late_query_results:
                cur = self.env['res.currency'].browse(result.get('currency'))
                number_late += 1
                sum_late += cur.compute(result.get('amount_total'), currency)
        prodd_obj = self.env['product.product'].search([])
        stock_objs = self.env['stock.move']       
        for prod in prodd_obj:
			tot_qty = 0
			tot_qty_in = 0
			tot_qty_out = 0

			dom = [('location_dest_id', 'child_of', 12), ('product_id','=', prod.id)]
			stocks_in = stock_objs.search( dom)
			if stocks_in:
				for stkIn in stocks_in:
					tot_qty_in += stkIn.product_uom_qty
			

			dom = [('location_id', 'child_of', 12), ('product_id','=', prod.id)]
			stocks_out = stock_objs.search( [ ('location_id', 'child_of', 12), ('product_id','=', prod.id)])
			if stocks_out:
				for stkOut in stocks_out:
					tot_qty_out += stkOut.product_uom_qty
			tot_qty=tot_qty_in - tot_qty_out
			if (tot_qty > 0 ):   			
				stock+=prod.purchase_price*tot_qty 	
			

        return {
            'number_to_reconcile': number_to_reconcile,
            'account_balance': self.formatLang(self.env, account_sum, currency_obj=self.currency.id or self.company_id.currency_id,digits=3),
            'last_balance': self.formatLang(self.env, last_balance, currency_obj=self.currency.id or self.company_id.currency_id,digits=3),
            'number_draft': number_draft,
            'number_waiting': number_waiting,
            'number_late': number_late,
            'sum_stock':self.formatLang(self.env, stock, currency_obj=self.currency.id or self.company_id.currency_id,digits=3),
            'sum_draft': self.formatLang(self.env, sum_draft or 0.0, currency_obj=self.currency.id or self.company_id.currency_id,digits=3),
            'sum_waiting': self.formatLang(self.env, sum_waiting or 0.0, currency_obj=self.currency.id or self.company_id.currency_id,digits=3),
            'sum_late': self.formatLang(self.env, sum_late or 0.0, currency_obj=self.currency.id or self.company_id.currency_id,digits=3),
            'currency_id': self.currency.id or self.company_id.currency_id.id,
            'bank_statements_source': False,
            'title': title,
        }

    @api.multi
    def action_create_new(self):
        ctx = self._context.copy()
        model = 'account.invoice'
        if self.type == 'sale':
            ctx.update({'journal_type': self.type, 'default_type': 'out_invoice', 'type': 'out_invoice', 'default_journal_id': self.id})
            if ctx.get('refund'):
                ctx.update({'default_type':'out_refund', 'type':'out_refund'})
            view_id = self.env.ref('account.invoice_form').id
        elif self.type == 'purchase':
            ctx.update({'journal_type': self.type, 'default_type': 'in_invoice', 'type': 'in_invoice', 'default_journal_id': self.id})
            if ctx.get('refund'):
                ctx.update({'default_type': 'in_refund', 'type': 'in_refund'})
            view_id = self.env.ref('account.invoice_supplier_form').id
        else:
            ctx.update({'default_journal_id': self.id})
            view_id = self.env.ref('account.view_move_form').id
            model = 'account.move'
        return {
            'name': _('Create invoice/bill'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': model,
            'view_id': view_id,
            'context': ctx,
        }

    @api.multi
    def create_cash_statement(self):
        ctx = self._context.copy()
        ctx.update({'journal_id': self.id, 'default_journal_id': self.id, 'default_journal_type': 'cash'})
        return {
            'name': _('Create cash statement'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.bank.statement',
            'context': ctx,
        }

    @api.multi
    def action_open_reconcile(self):
        if self.type in ['bank', 'cash']:
            # Open reconciliation view for bank statements belonging to this journal
            bank_stmt = self.env['account.bank.statement'].search([('journal_id', 'in', self.ids)])
            return {
                'type': 'ir.actions.client',
                'tag': 'bank_statement_reconciliation_view',
                'context': {'statement_ids': bank_stmt.ids},
            }
        else:
            # Open reconciliation view for customers/suppliers
            action_context = {'show_mode_selector': False}
            if self.type == 'sale':
                action_context.update({'mode': 'customers'})
            elif self.type == 'purchase':
                action_context.update({'mode': 'suppliers'})
            return {
                'type': 'ir.actions.client',
                'tag': 'manual_reconciliation_view',
                'context': action_context,
            }

    @api.multi
    def open_action(self):
        """return action based on type for related journals"""
        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.type == 'bank':
                action_name = 'action_bank_statement_tree'
            elif self.type == 'cash':
                action_name = 'action_view_bank_statement_tree'
            elif self.type == 'sale':
                action_name = 'action_invoice_tree1'
            elif self.type == 'purchase':
                action_name = 'action_invoice_tree2'
            else:
                action_name = 'action_move_journal_line'

        _journal_invoice_type_map = {
            'sale': 'out_invoice',
            'purchase': 'in_invoice',
            'bank': 'bank',
            'cash': 'cash',
            'general': 'general',
        }
        invoice_type = _journal_invoice_type_map[self.type]

        ctx = self._context.copy()
        ctx.update({
            'journal_type': self.type,
            'default_journal_id': self.id,
            'search_default_journal_id': self.id,
            'default_type': invoice_type,
            'type': invoice_type
        })
        ir_model_obj = self.pool['ir.model.data']
        model, action_id = ir_model_obj.get_object_reference(self._cr, self._uid, 'account', action_name)
        action = self.pool[model].read(self._cr, self._uid, action_id, context=self._context)
        action['context'] = ctx
        action['domain'] = self._context.get('use_domain', [])
        return action

    @api.multi
    def open_spend_money(self):
        return self.open_payments_action('outbound')

    @api.multi
    def open_collect_money(self):
        return self.open_payments_action('inbound')

    @api.multi
    def open_transfer_money(self):
        return self.open_payments_action('transfer')

    @api.multi
    def open_payments_action(self, payment_type):
        ctx = self._context.copy()
        ctx.update({
            'default_payment_type': payment_type,
            'default_journal_id': self.id
        })
        action_rec = self.env['ir.model.data'].xmlid_to_object('account.action_account_payments')
        if action_rec:
            action = action_rec.read([])[0]
            action['context'] = ctx
            action['domain'] = [('journal_id','=',self.id),('payment_type','=',payment_type)]
            return action

    @api.multi
    def open_action_with_context(self):
        action_name = self.env.context.get('action_name', False)
        if not action_name:
            return False
        ctx = dict(self.env.context, default_journal_id=self.id)
        if ctx.get('search_default_journal', False):
            ctx.update(search_default_journal_id=self.id)
        ir_model_obj = self.pool['ir.model.data']
        model, action_id = ir_model_obj.get_object_reference(self._cr, self._uid, 'account', action_name)
        action = self.pool[model].read(self._cr, self._uid, action_id, context=self._context)
        action['context'] = ctx
        if ctx.get('use_domain', False):
            action['domain'] = ['|', ('journal_id', '=', self.id), ('journal_id', '=', False)]
            action['name'] += ' for journal '+self.name
        return action

    @api.multi
    def create_bank_statement(self):
        """return action to create a bank statements. This button should be called only on journals with type =='bank'"""
        self.bank_statements_source = 'manual'
        action = self.env.ref('account.action_bank_statement_tree').read()[0]
        action.update({
            'views': [[False, 'form']],
            'context': "{'default_journal_id': " + str(self.id) + "}",
        })
        return action


    def formatLang(self, env, value, digits=None, grouping=True, monetary=False, dp=False, currency_obj=False):
        """
            Assuming 'Account' decimal.precision=3:
                formatLang(value) -> digits=2 (default)
                formatLang(value, digits=4) -> digits=4
                formatLang(value, dp='Account') -> digits=3
                formatLang(value, digits=5, dp='Account') -> digits=5
        """

        if digits is None:
            digits = DEFAULT_DIGITS = 3
            if dp:
                decimal_precision_obj = env['decimal.precision']
                digits = decimal_precision_obj.precision_get(dp)
            elif (hasattr(value, '_field') and isinstance(value._field, (float_field, function_field)) and value._field.digits):
                    digits = value._field.digits[1]
                    if not digits and digits is not 0:
                        digits = DEFAULT_DIGITS

        if isinstance(value, (str, unicode)) and not value:
            return ''

        lang = env.user.company_id.partner_id.lang or 'en_US'
        lang_objs = env['res.lang'].search([('code', '=', lang)])
        if not lang_objs:
            lang_objs = env['res.lang'].search([('code', '=', 'en_US')])
        lang_obj = lang_objs[0]

        res = lang_obj.format('%.' + str(digits) + 'f', value, grouping=grouping, monetary=monetary)

        #if currency_obj:
        #    res = '%s %s' % (currency_obj.symbol, res)
        return res
