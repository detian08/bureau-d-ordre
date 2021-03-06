# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

import openerp.addons.decimal_precision as dp
from openerp import pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import Number_To_Word
from openerp import  api, _

class invoice_picking(osv.osv):
	
   	def _amount_all(self, cr, uid, ids, name, args, context=None):
	    res = {}
	    var='Timbre'
            cr.execute('SELECT valeur FROM account_parametre WHERE designation=%s', (var,))
            timbre = cr.dictfetchone()['valeur'] 
	    print "timbre====",timbre 
            if timbre:
              for invoice in self.browse(cr,uid,ids, context=context):
                res[invoice.id] = {
                    'timbre':0.0,
                    'amount_untaxed': 0.0,
                    'undiscount_total': 0.0,
                    'discount_total': 0.0,
                    'amount_total': 0.0,
                } 
                cr.execute('SELECT * FROM invoice_picking_line WHERE invoice_picking_id=%s', (invoice.id,))
                line = cr.dictfetchall()
                for l in line:           
                    if l['amount_total'] != None:			            
                       res[invoice.id]['amount_untaxed']=res[invoice.id]['amount_untaxed']+l['amount_untaxed']
                       res[invoice.id]['amount_total']=res[invoice.id]['amount_total']+l['amount_total']
                       res[invoice.id]['undiscount_total']=res[invoice.id]['undiscount_total']+l['undiscount_total']
                       res[invoice.id]['discount_total']=res[invoice.id]['discount_total']+l['discount_total']
		if invoice.partner_id.timbre == True and invoice.type== 'out_invoice':
		    print "daaaans iff out_invoice"
               	    res[invoice.id]['amount_total'] += timbre
               	    res[invoice.id]['timbre'] = timbre
            	if invoice.partner_id.timbre == True and invoice.type== 'in_invoice' :
		    print "daaaans iff in_invoice"
               	    res[invoice.id]['amount_total'] += timbre
               	    res[invoice.id]['timbre'] = timbre
		if res[invoice.id]['amount_total'] != 0.0 :
                    amount_word=""
		    amount_word=Number_To_Word.Number_To_Word(res[invoice.id]['amount_total'], 'fr', 'Dinars', 'Millimes', 3)
                    cr.execute('UPDATE invoice_picking SET amount_word=%s WHERE id=%s', (amount_word, invoice.id))
            else:
                raise osv.except_osv(_('Paramètre Timbre inexistant!'), _('Vous devez ajouter le paramètre Timbre'))
	    return res

	def _amount_tax(self, cr, uid, ids, name, args, context=None):      
            val = {}
            for rec in self.browse(cr, uid, ids, context=context):
                val[rec.id] = 0.0
                cr.execute('SELECT * FROM invoice_picking_line WHERE invoice_picking_id=%s', (rec.id,))
                line = cr.dictfetchall()
                for l in line: 
                    cr.execute('SELECT * FROM stock_picking WHERE id=%s', (l['picking_id'],))
                    stock = cr.dictfetchall() 
                    for s in stock:
	                val[rec.id]=val[rec.id]+s['amount_tax']
	    return val

	def _get_type(self, cr, uid, context=None):
            if context is None:
               context = {}
            return context.get('type', 'out_invoice')

        def _get_currency(self, cr, uid, context=None):
          user = pooler.get_pool(cr.dbname).get('res.users').browse(cr, uid, [uid], context=context)[0]
          if user.company_id:
            return user.company_id.currency_id.id
          return pooler.get_pool(cr.dbname).get('res.currency').search(cr, uid, [('rate','=', 1.0)])[0]

	_name = "invoice.picking"
	_description = "invoice picking"
	_rec_name = "number"
        _order = "internal_number desc, id desc"

    	def _get_state_invoice(self, cr, uid, ids, field_name, arg, context=None):
          result = {}
          result = dict(map(lambda x: (x,''), ids))
          records = self.browse(cr, uid, ids)
          for r in records:
	        internal_number=r.internal_number
                result[r.id] = {'state_invoice': False} 
	        if internal_number:
        	  cr.execute('SELECT state FROM account_invoice WHERE internal_number=%s', (internal_number,))
	    	  str = cr.dictfetchone()
	    	  if str:   
                    result[r.id]= str['state']
    	  return result 

	_columns = {
		'internal_number': fields.char('Référence', size=32,help="Référence unique pour la facture",readonly=True),
		'number': fields.char('Code Facture', size=32,help="Référence unique pour la facture"),
		'ref_fournisseur':fields.char(' Référence Fournisseur ', size=100,help="Référence fournisseur"),
		'date_invoice_picking': fields.date('Date', required=True,),
		'partner_id': fields.many2one('res.partner', 'partner_id', ),
                'invoice_picking_line':fields.one2many('invoice.picking.line', 'invoice_picking_id', 'Ligne de Facture de Bon Livraison',readonly=True, states={'draft':[('readonly',False)]}),
		'amount_untaxed': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total NHT', method=True, store=True,multi='all'),
		'amount_tax': fields.function(_amount_tax, digits_compute=dp.get_precision('Account'), string='Impots et taxes', method=True,store=True),
		'discount_total': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total Remise', store=True, method=True, multi='all'),
		'undiscount_total': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total HT', store=True, method=True, multi='all'),
		'amount_total': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total TTC', store=True, method=True, multi='all'),
		'timbre': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Timbre', store=True, method=True,multi='all'),
		'user_id': fields.many2one('res.users', 'Salesman', ),
		'company_id': fields.many2one('res.company', 'Company', required=True, change_default=True, ),
		'currency_id': fields.many2one('res.currency', 'Devise', required=True, ),
		'state': fields.selection([('draft','Brouillon'),('open','Ouverte'), ('cancel', 'Annulée')],'Etat', select=True, ),
		'date': fields.char('Date Facture', size=254,states={'draft':[('readonly',False)]}, ),
		'amount_word': fields.char('Lettre', size=254),
		#'currency_id':	fields.many2one('res.currency', 'Devise',required=True ),
		'mode_reglement': fields.char('Mode de reglement ', size=254),#,required=True
		'tax_line': fields.one2many('invoice.picking.tax', 'invoice_id', 'Tax Lines',),          
		'type': fields.selection([('out_invoice','Customer Invoice'),('in_invoice','Supplier Invoice')],'Type', select=True, change_default=True),
		'date_due' :fields.date(string='Date d\'échéance',readonly=True, states={'draft': [('readonly', False)],'open': [('readonly', False)]},  copy=False),#required=True,
     		#'state_invoice': fields.function(_get_state_invoice, type="selection", selection= [('draft', 'Brouilon'),('ppaid','Patiellement Payee'),('paid','Payee'),('open', 'Ouverte'),], method=True, string='State',size=64),
			}

	_defaults = {
		'type': _get_type,
                'state': lambda *a: 'draft',
		'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'account.invoice', context=c),
                'internal_number': False,
                'number': False,
		'user_id': lambda s, cr, u, c: u,
		'currency_id': _get_currency,
	}

        def inv_open(self, cr, uid, ids, context=None):   
            self.write(cr, uid, ids, { 'state': 'open'})
            self.reset_taxes(cr, uid, ids, context)          
            internal_number_invoice = self.browse(cr, uid, ids[0]).internal_number      
            number_invoice = self.browse(cr, uid, ids[0]).number     
	    invoice_id = self.browse(cr, uid, ids[0]).id
	    cr.execute('SELECT picking_id FROM invoice_picking_line WHERE invoice_picking_id=%s', (ids[0],))
	    lines= cr.dictfetchall()
	    for line in lines:
		cr.execute('SELECT invoice_state,name FROM stock_picking WHERE id=%s', (line['picking_id'],))
	        lines_pick= cr.dictfetchall()
		cr.execute("update stock_picking SET number_invoice=%s,internal_number_invoice=%s,invoice_state='invoiced' WHERE id=%s", (number_invoice,internal_number_invoice,line['picking_id'],))
		for line_pick in lines_pick:
		  if line_pick['invoice_state']=='invoiced':
		    raise osv.except_osv(_('Un Bon de Reception a ete facture !'),_("Veuillez verifier le Bon de Reception numero %s" %line_pick['name'],))
		val = {}
		val['invoice_state']='invoiced'
		self.pool.get('stock.picking').write(cr, uid, line['picking_id'], val)
            id_inv=self._groupPickingsLines(cr, uid, ids[0],context)
            self._updatePicking(cr, uid, ids[0], id_inv, context)
	    cr.execute('SELECT * FROM invoice_picking WHERE id=%s', (invoice_id,))
	    invoice_line = cr.dictfetchall()[0]
	    amount_total =invoice_line['amount_total']
	    discount_total =invoice_line['discount_total']
	    amount_tax =invoice_line['amount_tax']
	    amount_untaxed = invoice_line['amount_untaxed']
	    undiscount_total = invoice_line['undiscount_total']
            #rimbd modif
            number = internal_number_invoice
            cr.execute('UPDATE account_invoice SET amount_total=%s,discount_total=%s,amount_untaxed=%s, amount_tax=%s, undiscount_total=%s,residual=%s,reste_a_payer=%s,number=%s WHERE id=%s', (amount_total,discount_total,amount_untaxed,amount_tax,undiscount_total,amount_total,amount_total,number, id_inv))
	    cr.execute('SELECT * FROM invoice_picking_tax WHERE invoice_id=%s',(ids[0],))
	    lines_tax= cr.dictfetchall()
	    for line in lines_tax:
	      tax_vals = {'invoice_id':id_inv,'name':line['name'],'account_id':line['account_id'],'base':line['base'],'amount':line['amount']}
              tax_id=self.pool.get('account.invoice.tax').create(cr, uid, tax_vals)
            cr.execute('UPDATE account_invoice SET amount_total=%s,discount_total=%s,amount_untaxed=%s, amount_tax=%s, undiscount_total=%s,residual=%s,number=%s WHERE id=%s', (amount_total,discount_total,amount_untaxed,amount_tax,undiscount_total,amount_total,number, id_inv))
	    return True

        def inv_draft(self, cr, uid, ids, context=None):
            self.write(cr, uid, ids, { 'state': 'draft' })
            return True

	def compute_taxes(self, cr, uid, ids, context=None):
            self.reset_taxes(cr, uid, ids, context)	
	    return True

	def reset_taxes(self, cr, uid, ids, context=None):

	    if context is None:
            	context = {}
            ctx = context.copy()
            ait_obj = self.pool.get('invoice.picking.tax')
            for id in ids:
            	cr.execute("DELETE FROM invoice_picking_tax WHERE invoice_id=%s AND manual is False", (id,))
            	partner = self.browse(cr, uid, id, context=ctx).partner_id
            	invoice = self.browse(cr, uid, id, context=ctx) 
		for taxe in ait_obj.compute(cr, uid, id, context=ctx).values():
                    ait_obj.create(cr, uid, taxe)
        	self.pool.get('invoice.picking').write(cr, uid, ids, {'invoice_picking_line':[]}, context=ctx)
	    return True


        def create(self, cr, uid, vals, context=None):
	    if context['type'] == 'out_invoice':
               vals['internal_number'] = self.pool.get('ir.sequence').get(cr, uid, 'invoice.out.reference')
	    if context['type'] == 'in_invoice':
               vals['internal_number'] = self.pool.get('ir.sequence').get(cr, uid, 'invoice.in.reference')
	    if vals['date_invoice_picking']:
               vals['date'] = vals['date_invoice_picking'].split("-")[2]+"/"+vals['date_invoice_picking'].split("-")[1]+"/"+vals['date_invoice_picking'].split("-")[0]
            res = super(invoice_picking,self).create(cr, uid, vals, context)
	    #cr.execute('SELECT amount_total FROM invoice_picking WHERE id=%s', (res,))
            return res
            
            

		        
		        
        def _groupPickingsLines(self, cr, uid, res,context=None):
	    
	    fbl = self.browse(cr, uid, res)
	    var='Timbre'
            timbre=0.00
	    if fbl.partner_id.timbre== True:
               cr.execute('SELECT valeur FROM account_parametre WHERE designation=%s', (var,))
               timbre = cr.dictfetchone()['valeur']  
            #Creation de la facture d articles relative a la facture de bls

	    invoice_obj = self.pool.get('account.invoice')

	    if fbl.type=='out_invoice':
	    	journal_id=1
	    elif fbl.type=='in_invoice':
	    	journal_id=2
	    else :
	    	journal_id=3


	    
            invoice_vals = {
		  'partner_id':fbl.partner_id.id,
		  'company_id':fbl.company_id.id,
		  'amount_tax':fbl.amount_tax,
		  'type':fbl.type,
		  'state':'open',
		  'journal_id':journal_id,
		  'internal_number':fbl.internal_number,
		  'account_id':562,
		  'date_invoice':fbl.date_invoice_picking,
		  'undiscount_total':fbl.undiscount_total,
		  'discount_total':fbl.discount_total,
		  'amount_untaxed':fbl.amount_untaxed,
		  'amount_total':fbl.amount_total,
		  'amount_tax':fbl.amount_tax,
		  'residual':fbl.amount_total,
		  'currency_id':fbl.currency_id.id,
		  'mode_reg':fbl.mode_reglement,
		  #'location_id':12,
		  'address_invoice_id':1,
		  'timbre':timbre,
                  #rim modif 07/05/2014 :: ref fsseur
                  'reference':fbl.number,
                  'supplier_invoice_number':fbl.number,
                  'supplier_invoice_number':fbl.ref_fournisseur,
                  'date_due':fbl.date_due,
                  #'discount':fbl.discount,
                  }
	    id_inv=invoice_obj.create(cr, uid, invoice_vals,context=context)
	    #--------------------------Regrouppement des articles des bons de livraison---------------------------------------------#

	    #Recuperer les articles relatis aux bls facturees
	    #cr.execute('select sm.*,smt.tax_id from stock_picking as sp, invoice_picking_line as ipl, stock_move as sm, stock_move_tax as smt '\
	#		'where ipl.picking_id=sp.id and sm.picking_id = sp.id and smt.move_id=sm.id and  ipl.invoice_picking_id=%s', (res,))
            cr.execute('select sm.* from stock_picking as sp, invoice_picking_line as ipl, stock_move as sm '\
			'where ipl.picking_id=sp.id and sm.picking_id = sp.id and  ipl.invoice_picking_id=%s', (res,))
	    lines= cr.dictfetchall()
	    invoice_line_obj = self.pool.get('account.invoice.line')
	    for line in lines:
		invoice_line_vals = {
                          'invoice_id':id_inv,
                          'name':  line['name'],
                          'product_id': line['product_id'],
                          'quantity':  line['product_qty'],
                          'discount':  line['discount'],
                          'default_code':  line['default_code'],
			  'price_unit': line['price_unit'],
			  'price_subtotal': line['price_subtotal'],
			  'account_id': 562,#1
			  #'account_id': 856,
			  'company_id': fbl.company_id.id
			}
                id_inv_line = invoice_line_obj.create(cr, uid, invoice_line_vals,context=context)
                
                
		if fbl.partner_id.exoner==False:
                    cr.execute('SELECT smt.tax_id FROM stock_move_tax AS smt WHERE smt.move_id=%s', (line['id'],))
                    taxes= cr.dictfetchall()
                    for taxe in taxes:
		        cr.execute('insert into account_invoice_line_tax values (%s,%s)',(id_inv_line,taxe['tax_id']))
                
	    return id_inv

	def _groupTaxPickingsLines(self, cr, uid, inv_id,context=None):
            
	    inv = self.browse(cr, uid, inv_id)
	    tax_obj=self.pool.get('account.invoice.tax')
            for taxe in tax_obj.compute(cr, uid, inv.id, context).values():
                tax_obj.create(cr, uid, taxe)
	    return True

        def _updatePicking(self, cr, uid, res, inv_id,context=None):
                        
	    cr.execute('select picking_id from invoice_picking_line where invoice_picking_id=%s ', (res,))
	    lines= cr.dictfetchall()
	    for line in lines:
		val = {}
		val['invoice_id']=inv_id
		val['state']='done'
		self.pool.get('stock.picking').write(cr, uid, line['picking_id'], val, context)
	    return True

invoice_picking()

class invoice_picking_line(osv.osv):

    _name = "invoice.picking.line"
    _description = "Invoice Picking Line"    
    _columns = {
        'amount_untaxed': fields.float('Total NHT', digits_compute=dp.get_precision('Account')),
	'amount_total': fields.float('TTC', digits_compute=dp.get_precision('Account'), store=True),
        'invoice_picking_id': fields.many2one('invoice.picking', 'Invoice Picking Reference', ondelete='cascade', select=True),
        'picking_id': fields.many2one('stock.picking', 'Bon Livraison', ondelete='cascade'),	
	'date_picking': fields.related('picking_id','date', type='date', relation='stock.picking', store=True, string='Date'),
	'discount_total': fields.float('Total Remise', digits_compute=dp.get_precision('Account')),
	'undiscount_total': fields.float('Total HT', digits_compute=dp.get_precision('Account')),
	'product_id': fields.related('picking_id','move_lines', type='many2many', relation='stock.move', string='Product'),
    }

    def picking_id_change(self, cr, uid, ids,picking_id, partner_id, context=None):	
	if not partner_id:
            raise osv.except_osv(_('Pas de partenaire choisi!'),_("Veuillez sélectionner un partenaire!") )
	res_final = {}
	if picking_id:
	    picking_obj = self.pool.get('stock.picking').browse(cr, uid, picking_id, context=context)
	    result = {}
	    result['amount_untaxed'] = picking_obj.amount_untaxed
	    result['date_picking'] = picking_obj.date
	    result['amount_total'] = picking_obj.amount_total
	    result['undiscount_total'] = picking_obj.undiscount_total
	    result['discount_total'] = picking_obj.discount_total
                
            res_final = {'value':result}
        return res_final

invoice_picking_line()

class stock_picking(osv.osv):
    _inherit = "stock.picking"
    _columns = {
	'invoice_picking_line': fields.one2many('invoice.picking.line', 'picking_id', 'Invoice Picking Line', ondelete='cascade', select=True), 
	}

stock_picking()

class invoice_picking_tax(osv.osv):
    _name = "invoice.picking.tax"
    _description = "Invoice Picking Tax"

    def _count_factor(self, cr, uid, ids, name, args, context=None):
        
        res = {}
        for invoice_tax in self.browse(cr, uid, ids, context=context):
            res[invoice_tax.id] = {
                'factor_base': 1.0,
                'factor_tax': 1.0,
            }
            if invoice_tax.amount <> 0.0:
                factor_tax = invoice_tax.tax_amount / invoice_tax.amount
                res[invoice_tax.id]['factor_tax'] = factor_tax

            if invoice_tax.base <> 0.0:
                factor_base = invoice_tax.base_amount / invoice_tax.base
                res[invoice_tax.id]['factor_base'] = factor_base             
       
        return res

    _columns = {
        'invoice_id': fields.many2one('invoice.picking', 'Invoice Line', ondelete='cascade', select=True),
        'name': fields.char('Tax Description', size=200, required=True),
        'account_id': fields.many2one('account.account', 'Tax Account', required=True, domain=[('type','<>','view'),('type','<>','income'), ('type', '<>', 'closed')]),
        'base': fields.float('Base', digits_compute=dp.get_precision('Account')),
        'amount': fields.float('Amount', digits_compute=dp.get_precision('Account')),
        'manual': fields.boolean('Manual'),
        'sequence': fields.integer('Sequence', help="Gives the sequence order when displaying a list of invoice tax."),
        'base_code_id': fields.many2one('account.tax.code', 'Base Code', help="The account basis of the tax declaration."),
        'base_amount': fields.float('Base Code Amount', digits_compute=dp.get_precision('Account')),
        'tax_code_id': fields.many2one('account.tax.code', 'Tax Code', help="The tax basis of the tax declaration."),
        'tax_amount': fields.float('Tax Code Amount', digits_compute=dp.get_precision('Account')),
        'company_id': fields.related('account_id', 'company_id', type='many2one', relation='res.company', string='Company', store=True, readonly=True),
        'factor_base': fields.function(_count_factor, method=True, string='Multipication factor for Base code', type='float', multi="all"),
        'factor_tax': fields.function(_count_factor, method=True, string='Multipication factor Tax code', type='float', multi="all")
    }

    def base_change(self, cr, uid, ids, base, currency_id=False, company_id=False, date_invoice=False):
        
        cur_obj = self.pool.get('res.currency')
        company_obj = self.pool.get('res.company')
        company_currency = False
        factor = 1
        if ids:
            factor = self.read(cr, uid, ids[0], ['factor_base'])['factor_base']
        if company_id:
            company_currency = company_obj.read(cr, uid, [company_id], ['currency_id'])[0]['currency_id'][0]
        if currency_id and company_currency:
            base = cur_obj.compute(cr, uid, currency_id, company_currency, base*factor, context={'date': date_invoice or time.strftime('%Y-%m-%d')}, round=False)             
        
        return {'value': {'base_amount':base}}

    def amount_change(self, cr, uid, ids, amount, currency_id=False, company_id=False, date_invoice=False):
        cur_obj = self.pool.get('res.currency')
        company_obj = self.pool.get('res.company')
        company_currency = False
        factor = 1
        if ids:
            factor = self.read(cr, uid, ids[0], ['factor_tax'])['factor_tax']
        if company_id:
            company_currency = company_obj.read(cr, uid, [company_id], ['currency_id'])[0]['currency_id'][0]
        if currency_id and company_currency:
            amount = cur_obj.compute(cr, uid, currency_id, company_currency, amount*factor, context={'date': date_invoice or time.strftime('%Y-%m-%d')}, round=False)             
        
        return {'value': {'tax_amount': amount}}

    _order = 'sequence'
    _defaults = {
        'manual': 1,
        'base_amount': 0.0,
        'tax_amount': 0.0,
    }
    def compute(self, cr, uid, invoice_id, context=None):
                   
        tax_grouped = {}
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        inv = self.pool.get('invoice.picking').browse(cr, uid, invoice_id, context=context)
        cur = inv.currency_id
        company_currency = inv.company_id.currency_id.id	
        cr.execute('SELECT * FROM invoice_picking_line WHERE invoice_picking_id=%s', (invoice_id,))	
        picking_id = cr.dictfetchall()
        for picking in picking_id :
	    moves = self.pool.get('stock.picking').browse(cr, uid, picking['picking_id'], context=context)
            for line in moves.move_lines:           
            	prod = self.pool.get('product.product').browse(cr, uid, line.product_id, context=context)
            	price=line.price_unit* (1-(line.discount or 0.0)/100.0)
            	for tax in tax_obj.compute_all(cr, uid, line.move_tax_id, price, line.product_qty, line.product_id, inv.partner_id)['taxes']:
                	val={}            
                	val['invoice_id'] = inv.id
                        #rimbd modif
               		#val['name'] = tax['name'][-5:].replace('-','')
                        val['name'] = tax['name']
                	val['amount'] = tax['amount']
                	val['manual'] = False
                	val['sequence'] = tax['sequence']
                	val['base'] = tax['price_unit'] * line['product_qty']
                	if moves.picking_type_id in (2,1):
                		val['base_code_id'] = tax['base_code_id']
                  		val['tax_code_id'] = tax['tax_code_id']
                    		val['base_amount'] = cur_obj.compute(cr, uid, inv.currency_id.id, company_currency, val['base'] * tax['base_sign'], context={'date': inv.date or time.strftime('%Y-%m-%d')}, round=False)
                    		val['tax_amount'] = cur_obj.compute(cr, uid, inv.currency_id.id, company_currency, val['amount'] * tax['tax_sign'], context={'date': inv.date or time.strftime('%Y-%m-%d')}, round=False)
                    		val['account_id'] = tax['account_collected_id'] or line['account_id'].id
                	else:
                    		val['base_code_id'] = tax['ref_base_code_id']
                    		val['tax_code_id'] = tax['ref_tax_code_id']
                    		val['base_amount'] = cur_obj.compute(cr, uid, inv.currency_id.id, company_currency, val['base'] * tax['ref_base_sign'], context={'date': inv.date or time.strftime('%Y-%m-%d')}, round=False)
                    		val['tax_amount'] = cur_obj.compute(cr, uid, inv.currency_id.id, company_currency, val['amount'] * tax['ref_tax_sign'], context={'date': inv.date or time.strftime('%Y-%m-%d')}, round=False)
                    		val['account_id'] = tax['account_paid_id'] or line['account_id'].id

                	key = (val['tax_code_id'], val['base_code_id'], val['account_id'])
                	if not key in tax_grouped:
                  		tax_grouped[key] = val
               		else:
                    		tax_grouped[key]['amount'] += val['amount']
                    		tax_grouped[key]['base'] += val['base']
                    		tax_grouped[key]['base_amount'] += val['base_amount']
                    		tax_grouped[key]['tax_amount'] += val['tax_amount']
        return tax_grouped


    def move_line_get(self, cr, uid, invoice_id):
        
        res = []
        cr.execute('SELECT * FROM account_invoice_tax WHERE invoice_id=%s', (invoice_id,))
        for t in cr.dictfetchall():
            if not t['amount'] \
                    and not t['tax_code_id'] \
                    and not t['tax_amount']:
                continue
           
            res.append({
                'type':'tax',
                'name':t['name'],
                'price_unit': t['amount'],
                'quantity': 1,
                'price': t['amount'] or 0.0,
                'account_id': t['account_id'],
                'tax_code_id': t['tax_code_id'],
                'tax_amount': t['tax_amount']
            })             
       
        return res

invoice_picking_tax()
