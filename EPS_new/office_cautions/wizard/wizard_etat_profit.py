# -*- coding: utf-8 -*-
import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime
from openerp import api

class wizard_etat_profit(osv.osv_memory):
	_name = "wizard.etat.profit"
	_description = "Etat Profit Wizard "

	#def _calculer_stock(self, cr, uid, ids, field_name, arg, context):
	#res = {}
	#print "dans calculer stock "
	#for wizard in self.browse(cr, uid, ids, context=context):
		#print "dans foooorrr"
		#res[wizard.id] =100
	#return res



	_columns = { 
		#'caisse_id':fields.many2one('account.bank.statement', 'Caisse',required=True),
		'date_debut': fields.date('Date ', required=True, select=True), 
		#'date_fin': fields.date('Date Fin', required=True, select=True),
		'date_aujourd': fields.date('Date ', required=True, select=True),
		'compte_biat': fields.float('Compte BIAT', digits_compute= dp.get_precision('Account'),),
		'compte_zitouna': fields.float('Compte Zitouna', digits_compute= dp.get_precision('Account'),),
		'cheque_antidates': fields.float('Cheques antidates',help="Les Chéques Clients intégrés et non encaissés,leurs dates d'échéance supérieur à la date d'aujourd'hui  " ,digits_compute= dp.get_precision('Account'),readonly=True),
		'factures_clients': fields.float('Factures Clients',help="Factures Clients non payés, leurs dates inférieur à la date choisie" , digits_compute= dp.get_precision('Account'),readonly=True),
		'solde_caisse': fields.float('Solde Caisses Ouvertes',help="Solde de toutes les caisses ouvertes" , digits_compute= dp.get_precision('Account'),readonly=True),
		'cheque_circ': fields.float('Cheques en circulation',help="Les Chéques Fournisseurs intégrés et non encaissés  " , digits_compute= dp.get_precision('Account'),readonly=True),
		'cheque_dep': fields.float('Cheques depenses',
									help="Les Chéques depense et non encaissées  ",
									digits_compute=dp.get_precision('Account'), readonly=True),
		'avoir': fields.float('Avoir client',
								   digits_compute=dp.get_precision('Account'), readonly=True),
		'fact_etrangr': fields.float('Facture Fournisseurs Etrangere',help="Factures Fournisseurs Etrangéres non payés, leurs dates inférieur à la date choisie" , digits_compute= dp.get_precision('Account'),readonly=True),
		'fact_locaux': fields.float('Facture Fournisseurs Locaux',help="Factures Fournisseurs Locaux non payés, leurs dates inférieur à la date choisie" , digits_compute= dp.get_precision('Account'),readonly=True),
		'stock': fields.float('Stock', help="La somme de prix d'achat de tous les Articles dans le stock " ,digits_compute= dp.get_precision('Account'),readonly=True),
		#'stock':fields.function(_calculer_stock, type="float", method=True),
		'caution':fields.float('Cautions et Garantie',help="Les Cautions et Garanties non libérés et leurs dates inférieur à la date choisie" , digits_compute= dp.get_precision('Account'),readonly=True),

	}
	_defaults = {
		'date_debut': fields.datetime.now,
		'date_aujourd': fields.datetime.now,
		'factures_clients': 0.00,
		'cheque_antidates':0.00,
		'solde_caisse':0.00,
		'avoir': 0.00,
	}




	def create_report(self, cr, uid, ids, context={}):
		data = self.read(cr,uid,ids,)[0]
		#data = self.read(cr,uid,ids,)[-1] 
		print data,' create_report('
		res={}
		res={
				'type'         : 'ir.actions.report.xml',
				'report_name'   : 'jasper_etat_profit_print',
				'datas': {
				        'model':'wizard.etat.profit',
				        'id': context.get('active_ids') and context.get('active_ids')[0] or False,
				        'ids': context.get('active_ids') and context.get('active_ids') or [],
				        
				        'form':data
				        },
				'nodestroy': False
			}
		return res


	def calculer(self, cr, uid,ids,date_debut,date_aujourd,context=None):

		res ={}
		res_final = {}

#----------------------------------------------------------------------------------------------------------

		#montant facture clients non payées

#----------------------------------------------------------------------------------------------------------
		factures_clients=0
		#,('state','not in',['paid']
		fact_ids = self.pool.get('account.invoice').search(cr, uid, [('date_invoice','<=',date_debut),('type','=','out_invoice'),('state', '!=', 'cancel')])
		fact_objs = self.pool.get('account.invoice').browse(cr, uid, fact_ids)
		inv_pick_ids = self.pool.get('invoice.picking').search(cr, uid, [('date_invoice_picking','<=',date_debut),('type','=','out_invoice'),
																		 ('state', '=', 'draft')])
		inv_pick_objs = self.pool.get('invoice.picking').browse(cr, uid, inv_pick_ids)

		res['factures_clients'] =factures_clients

		if fact_objs:
			for fact in fact_objs:
				montant_reg=0
				#maroua T modif 08/12/2016 comment this line (ajouter or fact.state=='ppaid')
				if fact.state=='paid' or fact.state=='ppaid':
					reg_ids=self.pool.get('reglement.detail').search(cr, uid, [('invoice_id','=',fact.id),('reglement_id.date_reglement','>',date_debut)])
					reg_objs = self.pool.get('reglement.detail').browse(cr, uid, reg_ids)
					for reg in reg_objs:
						#print "*********************************",reg.reglement_id.date_reglement
						montant_reg+=reg.montant
						print"aaaaaaaaaaaa,montant_reg", montant_reg

					factures_clients+=montant_reg
				
				else :
					print "facture client ==", fact.reste_a_payer
					factures_clients+=fact.reste_a_payer
				print"aaaaaaaaaaaa,factures_clients1", factures_clients
				#maroua T modif 08/12/2016 comment this line (ajouter if fact.state=='ppaid':)
				if fact.state=='ppaid':
					factures_clients+=fact.reste_a_payer
					print"aaaaaaaaaaaa,factures_clients2", factures_clients

				if fact.state == 'draft':
					factures_clients += fact.amount_total
				print"aaaaaaaaaaaa,factures_clients3", factures_clients
					#print "fact client PPAID **********===============",fact.number
					#print "montant**************===============",fact.reste_a_payer
					
				#maroua T modif 08/12/2016 comment this line			
				#elif fact.state=='draft':
				#	factures_clients+=fact.amount_total
				#else:	
				#	factures_clients+=fact.reste_a_payer
				#maroua T modif 08/12/2016 comment this line


			res['factures_clients'] =factures_clients	
		if inv_pick_objs:
			for inv_pick in inv_pick_objs  :
				print "facture client ==", inv_pick.amount_total

				factures_clients+=inv_pick.amount_total
			res['factures_clients'] =factures_clients

# ----------------------------------------------------------------------------------------------------------

		# montant cheque antidates

# ----------------------------------------------------------------------------------------------------------


		cheque_antidates=0
		res['cheque_antidates'] =cheque_antidates
		pieces_ids = self.pool.get('reglement.piece').search(cr, uid, [('mode_reglement','=','Chèque'),('type','=','out')])#,('state','in',['integrated'])]) 
		# ('date_echance','>',date_aujourd),  
		pieces_objs = self.pool.get('reglement.piece').browse(cr, uid, pieces_ids)
		if pieces_objs:
			#print "pieces_objs=============",pieces_objs
			for piece in pieces_objs:
				#print "piece **********===============",piece
				#print "montant**************===============",piece.montant_monnaie_local

				#,('state','in',['integrated'])]
				if piece.state=='integrated' or (piece.state=='cashed' and piece.date_encaissement > date_debut):
					cheque_antidates=cheque_antidates+piece.montant_monnaie_local
			res['cheque_antidates'] =cheque_antidates

# ----------------------------------------------------------------------------------------------------------

# montant avoir client add by salwa le 23/05/2017

# ----------------------------------------------------------------------------------------------------------

			avoir = 0
		fact_ids = self.pool.get('account.invoice').search(cr, uid, [('date_invoice', '<=', date_debut),
																	('type', '=', 'out_refund'),
																	('state', '!=', 'cancel')])
		fact_objs = self.pool.get('account.invoice').browse(cr, uid, fact_ids)
		res['avoir'] = avoir

		if fact_objs:
			for fact in fact_objs:
				montant_reg = 0
				# maroua T modif 08/12/2016 comment this line (ajouter or fact.state=='ppaid')
				if fact.state == 'paid' or fact.state == 'ppaid':
					reg_ids = self.pool.get('reglement.detail').search(cr, uid, [('invoice_id', '=', fact.id), (
					'reglement_id.date_reglement', '>', date_debut)])
					reg_objs = self.pool.get('reglement.detail').browse(cr, uid, reg_ids)
					for reg in reg_objs:
						# print "*********************************",reg.reglement_id.date_reglement
						montant_reg += reg.montant
						print"bbbbbbbbbbbbbbbbbbb,montant_reg", montant_reg

						avoir += montant_reg
				else:
					print "facture client ==", fact.reste_a_payer
					avoir += fact.reste_a_payer
				print"bbbbbbbbbbbbbbbbbbb,avoir", avoir
				# maroua T modif 08/12/2016 comment this line (ajouter if fact.state=='ppaid':)
				if fact.state == 'ppaid':
					avoir += fact.reste_a_payer
					print"bbbbbbbbbbbbbbbbbbb,avoir", avoir

				if fact.state == 'draft':
					avoir += fact.amount_total
					print"bbbbbbbbbbbbbbbbbbb,avoir", avoir
			res['avoir'] = avoir


		# if reg_objs:
		# 	for reg in reg_objs:
		# 		avoir = avoir + reg.amount_total
		# res['avoir'] = avoir

# ----------------------------------------------------------------------------------------------------------

		#solde caisse ouverte
		###solde_caisse=0  ###maroua T modif 16/12/2016 comment Le probleme c que le solde d'ouverture n'est pas 0
# ----------------------------------------------------------------------------------------------------------

		solde_caisse=108.466
		res['solde_caisse'] =solde_caisse
		cash_ids = self.pool.get('account.bank.statement.line').search(cr, uid, [('date','<=',date_debut)])
		cash_objs = self.pool.get('account.bank.statement.line').browse(cr, uid, cash_ids)
		if cash_objs:
			for cash in cash_objs:
				#print "date========", cash.date, " name========", cash.name, " solde========", cash.amount
				solde_caisse=solde_caisse+cash.amount
			res['solde_caisse'] =solde_caisse
# ----------------------------------------------------------------------------------------------------------
		#montant cheque en circulation ('date_encaissement','<',date_debut),
# ----------------------------------------------------------------------------------------------------------

		cheque_circ=0
		res['cheque_circ'] =cheque_circ
		cheq_ids = self.pool.get('reglement.piece').search(cr, uid, [('mode_reglement','=','Chèque'),('type','=','in')])#, ('state','in',['integrated'])])
		cheq_objs = self.pool.get('reglement.piece').browse(cr, uid, cheq_ids)
		if cheq_objs:
			for cheq in cheq_objs:
				#,('state','in',['integrated'])]
				if cheq.state=='integrated' or (cheq.state=='cashed' and cheq.date_encaissement > date_debut):
					cheque_circ=cheque_circ+cheq.montant_monnaie_local

			res['cheque_circ'] =cheque_circ

# ----------------------------------------------------------------------------------------------------------

# Créer par salwa ksila ; montant cheque depense

# ----------------------------------------------------------------------------------------------------------


			cheque_dep = 0
			res['cheque_dep'] =cheque_dep
			cheq_dep_ids = self.pool.get('office.cheque').search(cr, uid, [])
			cheq_objs = self.pool.get('office.cheque').browse(cr, uid, cheq_dep_ids)
			if cheq_objs:
				for cheq in cheq_objs:
					if cheq.state == "encaisse" :
						if cheq.date_echance <= date_debut and cheq.date_encaissement > date_debut:
							cheque_dep = cheque_dep + cheq.montant_monnaie_local
					else:
						if cheq.date_echance <= date_debut:
							cheque_dep = cheque_dep + cheq.montant_monnaie_local


					# if cheq.date_echance <= date_debut or cheq.date_encaissement and date_debut < cheq.date_encaissement:

				res['cheque_dep'] = cheque_dep


		# Créer par Salwa ksila ; montant cheque depense ('date_encaissement','<',date_debut),
		# cheque_dep = 0
		# res['cheque_dep'] =cheque_dep
		# cheq_line_obj = self.pool.get('office.cheque')
		# cheq_line_ids = cheq_line_obj.search(cr, uid, [])
		# for cheq_line_id in cheq_line_ids:
		# 	line = cheq_line_obj.browse(cr, uid, cheq_line_id, context=context)
		# 	if cheq.state == 'emis' and  date_debut < cheq.date_encaissement:
		# 			cheque_dep = cheque_dep + cheq.montant_monnaie_local
		# 	res['cheque_dep'] = cheque_dep


# ----------------------------------------------------------------------------------------------------------

# factures fourns entrangere

# ----------------------------------------------------------------------------------------------------------

		fact_etrangr=0
		res['fact_etrangr'] =fact_etrangr
		facture_ids = self.pool.get('account.invoice').search(cr, uid, [('date_invoice','<=',date_debut),('type','=','in_invoice'),('currency_id.name','!=','TND'),('partner_id.name','!=','EPS')])#
			
		facture_objs = self.pool.get('account.invoice').browse(cr, uid, facture_ids)
		if facture_objs:		
			for facture in facture_objs:

				currency=facture.currency_id.id,
				currency_obj = self.pool.get('res.currency').browse(cr,uid,currency,context=context)
				montant_reg=0
				if facture.state=='paid' or facture.state=='ppaid':
					reg_ids=self.pool.get('reglement.detail').search(cr, uid, [('invoice_id','=',facture.id),('reglement_id.date_reglement','>',date_debut)])
					reg_objs = self.pool.get('reglement.detail').browse(cr, uid, reg_ids)
					for reg in reg_objs:
						#print "*********************************",reg.reglement_id.date_reglement
						montant_reg+=reg.montant

					fact_etrangr+=(montant_reg/currency_obj.rate_silent)

				else :
					fact_etrangr+=(facture.reste_a_payer/currency_obj.rate_silent)
				if facture.state=='ppaid':
					fact_etrangr+=(facture.reste_a_payer/currency_obj.rate_silent)

				#elif facture.state=='draft':
				#	fact_etrangr+=(facture.amount_total/currency_obj.rate_silent)
				#else :
				#	fact_etrangr+=(facture.reste_a_payer/currency_obj.rate_silent)
				#print "fact_etrangr=====",fact_etrangr


			res['fact_etrangr'] =fact_etrangr
		inv_picking_ids = self.pool.get('invoice.picking').search(cr, uid, [('date_invoice_picking','<=',date_debut),('state','=','draft'),('type','=','in_invoice'),('currency_id','!=',137),('partner_id.name','!=','EPS')])
		inv_picking_etrg_objs = self.pool.get('invoice.picking').browse(cr, uid, inv_picking_ids)		
		if inv_picking_etrg_objs:
			for inv_picking in inv_picking_etrg_objs  :
					currency_obj = self.pool.get('res.currency').browse(cr,uid,inv_picking.currency_id.id,context=context)
					fact_etrangr+=(inv_picking.amount_total/currency_obj.rate_silent)
			res['fact_etrangr'] =fact_etrangr

# ----------------------------------------------------------------------------------------------------------

# facture fourns locaux

# ----------------------------------------------------------------------------------------------------------

		local_ids = self.pool.get('account.invoice').search(cr, uid, [('date_invoice','<=',date_debut),
																	  ('type','=','in_invoice'),
																	  # ('state', '!=', 'paid'),
																	  ('currency_id','=', 137),
																	  ('partner_id.name','!=','EPS')])

		local_objs = self.pool.get('account.invoice').browse(cr, uid, local_ids)

		print "local_objs=====================",local_objs
		fact_locaux=0
		res['fact_locaux'] =fact_locaux
		if local_objs:
			for facture in local_objs:
				montant_reg=0
				if facture.state=='paid' or facture.state=='ppaid':
					reg_ids=self.pool.get('reglement.detail').search(cr, uid, [('invoice_id','=',facture.id),('reglement_id.date_reglement','>',date_debut)])
					reg_objs = self.pool.get('reglement.detail').browse(cr, uid, reg_ids)
					for reg in reg_objs:
						#print "*********************************",reg.reglement_id.date_reglement
						montant_reg+=reg.montant

					fact_locaux+=montant_reg

				else :
					print"***************fact_locaux", fact_locaux

					fact_locaux+=facture.reste_a_payer
					print"***************fact_locaux2", fact_locaux

				if facture.state=='ppaid':
					print"***************fact_locaux3", fact_locaux

					fact_locaux+=facture.reste_a_payer
				if facture.state == 'draft':
					print"***************fact_locaux33", fact_locaux

					fact_locaux += facture.reste_a_payer


			res['fact_locaux'] =fact_locaux
		inv_picking_ids_wiz = self.pool.get('invoice.picking').search(cr, uid, [('state', '=', 'draft'),
																				('type', '=', 'in_invoice'),
																				('currency_id', '=', 137),
																				('partner_id.name', '!=', 'EPS')])#('date_invoice_picking','<=',date_debut)
		inv_picking_objs_wiz = self.pool.get('invoice.picking').browse(cr, uid, inv_picking_ids_wiz)
		for inv_wiz in inv_picking_objs_wiz:
			print"***************amount_total_wiz", inv_wiz.amount_total

		if inv_picking_objs_wiz:
			for inv in inv_picking_objs_wiz  :

				print"============inv_picking_ids_wiz", inv_picking_objs_wiz
				print"***************fact_locaux4", fact_locaux

				fact_locaux+= inv.amount_total
				print"***************fact_locaux5", fact_locaux

			res['fact_locaux'] =fact_locaux

# ----------------------------------------------------------------------------------------------------------

# Stock  travail Maroua T du 19-12-2016

# ----------------------------------------------------------------------------------------------------------
		#### Stock  travail Maroua Romdhane
		##stock=0
		##quant_obj = self.pool.get("stock.quant")
		##products_ids = self.pool.get('product.product').search(cr, uid, [])
		##products = self.pool.get('product.product').browse(cr, uid, products_ids)
		##for product in products:
		##	dom = [('in_date', '<=', date_debut), ('location_id', 'child_of', 12), ('product_id','=', product.id)]
		##	quants = quant_obj.search(cr, uid, dom)
		##	tot_qty = 0
		##	tot_qty_in = 0
		##	tot_qty_out = 0
		##	for quant in quant_obj.browse(cr, uid, quants, context=context):
		##		tot_qty_in += quant.qty
			
		##	quants_out = quant_obj.search(cr, uid, [('in_date', '<=', date_debut), ('location_id', 'child_of', 9), ('product_id','=', product.id)])
		##	for quant in quant_obj.browse(cr, uid, quants_out, context=context):
		##		tot_qty_out += quant.qty
		##	tot_qty=tot_qty_in - tot_qty_out
		##	if (tot_qty > 0 ):
		
		##		stock=stock+(product.purchase_price*tot_qty)
		##res['stock'] =stock
		##### Stock  travail Maroua Romdhane



		# Stock  travail Maroua T du 19-12-2016
		stock=0
		res['stock'] =stock
		stock_objs = self.pool.get("stock.move")
		products_ids = self.pool.get('product.product').search(cr, uid, [])
		products = self.pool.get('product.product').browse(cr, uid, products_ids)
		for product in products:
			tot_qty = 0
			tot_qty_in = 0
			tot_qty_out = 0

			## Entrée du stock
			dom = [('date', '<=', date_debut), ('location_dest_id', 'child_of', 12), ('product_id','=', product.id)]
			stocks_in = stock_objs.search(cr, uid, dom)
			for stkIn in stock_objs.browse(cr, uid, stocks_in, context=context):
				tot_qty_in += stkIn.product_uom_qty
			
			## Sortie du stock
			dom = [('date', '<=', date_debut), ('location_id', 'child_of', 12), ('product_id','=', product.id)]
			stocks_out = stock_objs.search(cr, uid, dom)
			for stkOut in stock_objs.browse(cr, uid, stocks_out, context=context):
				tot_qty_out += stkOut.product_uom_qty
			
			tot_qty = tot_qty_in - tot_qty_out
			if (tot_qty > 0 ):
				#print "*** Product***",product.default_code, " ****",product.name
				#print "*** Product Qty IN******",tot_qty_in, "*** Product Qty OUT****",tot_qty_out
				#print "*** Product Qty********",tot_qty
				#print "Prix revient******", product.purchase_price
				stock=stock+(product.purchase_price * tot_qty)
				res['stock'] =stock
				#print "***#####***"
		res['stock'] =stock

# ----------------------------------------------------------------------------------------------------------
	# cautions et garantie date_liberation ('date_caution','<=',date_debut),('libere','=',False)
	#update by salwa caut.date_caution <= date_debut)
#  ----------------------------------------------------------------------------------------------------------

		# cautions et garantie date_liberation ('date_caution','<=',date_debut),('libere','=',False)
		#update by salwa caut.date_caution <= date_debut)
		caution_ids = self.pool.get('office.caution').search(cr, uid, [])
			
		caution_objs = self.pool.get('office.caution').browse(cr, uid, caution_ids)
		caution=0
		res['caution'] =caution
		if caution_objs:
			for caut in caution_objs:

				if caut.libere == False and caut.date_caution <= date_debut:
					caution = caution + caut.montant

				elif caut.libere and caut.date_liberation > date_debut and caut.date_caution <= date_debut:
					caution=caution+caut.montant
				# else :
				# 	caution=caution+caut.montant
			res['caution'] =caution


		res_final = {'value':res}
		return res_final


  
wizard_etat_profit()
