# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import JasperDataParser  
from openerp.jasper_reports import jasper_report
from openerp import pooler
import time
from datetime import datetime
import base64
import os
#import netsvc
from openerp.osv import fields, osv
from openerp.tools.translate import _

class jasper_client(JasperDataParser.JasperDataParser):
    def __init__(self, cr, uid, ids, data, context):
        super(jasper_client, self).__init__(cr, uid, ids, data, context)

    def generate_data_source(self, cr, uid, ids, data, context):
        return 'records'

    def generate_parameters(self, cr, uid, ids, data, context):
        return {}

    def generate_properties(self, cr, uid, ids, data, context):
        return {}

    def generate_records(self, cr, uid, ids, data, context):
        pool= pooler.get_pool(cr.dbname)
        result=[]
        if 'form' in data:
            date_aujourd = data['form']['date_aujourd']
            #date_fin  = data['form']['date_fin']
            date_debut = data['form']['date_debut']
            compte_biat = data['form']['compte_biat']
            compte_zitouna= data['form']['compte_zitouna']
            total=0
#---------------------------------------------------------------------------------------------------------------
            ####debut
            #montant facture clients non payées
#----------------------------------------------------------------------------------------------------------------
            factures_clients=0
            fact_ids = self.pool.get('account.invoice').search(cr, uid, [('date_invoice','<=',date_debut),('type','=','out_invoice'), ('state', '!=', 'cancel')])
            fact_objs = self.pool.get('account.invoice').browse(cr, uid, fact_ids)
            inv_pick_ids = self.pool.get('invoice.picking').search(cr, uid, [('date_invoice_picking','<=',date_debut), ('state', '=', 'draft'),('type','=','out_invoice')])
            inv_pick_objs = self.pool.get('invoice.picking').browse(cr, uid, inv_pick_ids)

	        # res['factures_clients'] =factures_clients
	        
	        	        
            if fact_objs:
                for fact in fact_objs:
                    montant_reg=0
                    if fact.state=='paid' or fact.state=='ppaid':
                        reg_ids=self.pool.get('reglement.detail').search(cr, uid, [('invoice_id','=',fact.id),('reglement_id.date_reglement','>',date_debut)])
                        reg_objs = self.pool.get('reglement.detail').browse(cr, uid, reg_ids)
                        for reg in reg_objs:
	                        montant_reg+=reg.montant

                        factures_clients+=montant_reg
                    else :
                        # print "facture client ==", fact.reste_a_payer
                        factures_clients+=fact.reste_a_payer
                    if fact.state=='ppaid':	
                        factures_clients+=fact.reste_a_payer
                    if fact.state == 'draft':
                        factures_clients += fact.amount_total
            if inv_pick_objs:
                for inv_pick in inv_pick_objs  :
                    # print "facture client ==", inv_pick.amount_total
                    factures_clients+=inv_pick.amount_total                  
                        
                        
		        # res['factures_clients'] =factures_clients
#----------------------------------------------------------------------------------------------------------------

	        #montant cheque antidates

#----------------------------------------------------------------------------------------------------------------
            cheque_antidates=0
	        #res['cheque_antidates'] =cheque_antidates
            pieces_ids = self.pool.get('reglement.piece').search(cr, uid, [('mode_reglement','=','Chèque'),('type','=','out')])#,('state','in',['integrated'])]) 
            pieces_objs = self.pool.get('reglement.piece').browse(cr, uid, pieces_ids)
            if pieces_objs:
                for piece in pieces_objs:
                    if piece.state=='integrated' or (piece.state=='cashed' and piece.date_encaissement > date_debut):
					    cheque_antidates=cheque_antidates+piece.montant_monnaie_local

		        #res['cheque_antidates'] =cheque_antidates

# ----------------------------------------------------------------------------------------------------------

# montant avoir client add by salwa le 23/05/2017

# ----------------------------------------------------------------------------------------------------------

            avoir = 0
            fact_ids = self.pool.get('account.invoice').search(cr, uid, [('date_invoice', '<=', date_debut),
                                                                         ('type', '=', 'out_refund'),
                                                                         ('state', '!=', 'cancel')])
            fact_objs = self.pool.get('account.invoice').browse(cr, uid, fact_ids)

            if fact_objs:
                for fact in fact_objs:
                    montant_reg = 0
                    # maroua T modif 08/12/2016 comment this line (ajouter or fact.state=='ppaid')
                    if fact.state == 'paid' or fact.state == 'ppaid':
                        reg_ids = self.pool.get('reglement.detail').search(cr, uid, [('invoice_id', '=', fact.id),
                                                                                     ('reglement_id.date_reglement', '>', date_debut)])
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
            # # res['avoir'] = avoir
            # reg_ids = self.pool.get('account.invoice').search(cr, uid, [('type', '=', 'out_refund'),
            #                                                             ('state', '!=', 'paid')])
            # reg_objs = self.pool.get('account.invoice').browse(cr, uid, reg_ids)
            # if reg_objs:
            #     for reg in reg_objs:
            #         avoir = avoir + reg.amount_total
                # res['avoir'] = avoir


                    #--------------------------------------------------------------------------------------------------------------

	        #solde caisse ouverte
    #--------------------------------------------------------------------------------------------------------------
            solde_caisse=108.466
	        #res['solde_caisse'] =solde_caisse
            cash_ids = self.pool.get('account.bank.statement.line').search(cr, uid, [('date','<=',date_debut)])
            cash_objs = self.pool.get('account.bank.statement.line').browse(cr, uid, cash_ids)
            if cash_objs:
                for cash in cash_objs:
                    solde_caisse=solde_caisse+cash.amount
		        #res['solde_caisse'] =solde_caisse

	#------------------------------------------------------------------------------------------------------------
	        #montant cheque en circulation
    #------------------------------------------------------------------------------------------------------------
            cheque_circ=0
	        #res['cheque_circ'] =cheque_circ('date_encaissement','<',date_debut)
            cheq_ids = self.pool.get('reglement.piece').search(cr, uid, [('mode_reglement','=','Chèque'),('type','=','in')])
                    
            cheq_objs = self.pool.get('reglement.piece').browse(cr, uid, cheq_ids)
            if cheq_objs:
                for cheq in cheq_objs:
                    if cheq.state=='integrated' or (cheq.state=='cashed' and cheq.date_encaissement > date_debut):
                        cheque_circ=cheque_circ+cheq.montant_monnaie_local
		        #res['cheque_circ'] =cheque_circ

#-----------------------------------------------------------------------------------------------------------------

#factures fourns entrangere

#----------------------------------------------------------------------------------------------------------------
            fact_etrangr=0
	        #res['fact_etrangr'] =fact_etrangr
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
	                        montant_reg+=reg.montant

                        fact_etrangr+=(montant_reg/currency_obj.rate_silent)
                    else :
                        fact_etrangr+=(facture.reste_a_payer/currency_obj.rate_silent)
                    if facture.state=='ppaid':
                        fact_etrangr+=(facture.reste_a_payer/currency_obj.rate_silent)
            inv_picking_ids = self.pool.get('invoice.picking').search(cr, uid, [('date_invoice_picking','<=',date_debut),('state','=','draft'),('type','=','in_invoice'),('currency_id','!=',137),('partner_id.name','!=','EPS')])
            
            inv_picking_etrg_objs = self.pool.get('invoice.picking').browse(cr, uid, inv_picking_ids)		
            if inv_picking_etrg_objs:
                for inv_picking in inv_picking_etrg_objs  :
                    currency_obj = self.pool.get('res.currency').browse(cr,uid,inv_picking.currency_id.id,context=context)
                    fact_etrangr+=(inv_picking.amount_total/currency_obj.rate_silent)

#--------------------------------------------------------------------------------------------------------

#facture fourns locaux

#--------------------------------------------------------------------------------------------------------

            local_ids = self.pool.get('account.invoice').search(cr, uid, [('date_invoice','<=',date_debut),
                                                                          ('type','=','in_invoice'),
                                                                          ('currency_id.name','=','TND'),
                                                                          ('partner_id.name','!=','EPS')])
                    
            local_objs = self.pool.get('account.invoice').browse(cr, uid, local_ids)
            fact_locaux=0
	        #res['fact_locaux'] =fact_locaux
            if local_objs:
                for facture in local_objs:
                    montant_reg=0
                    if facture.state=='paid' or facture.state=='ppaid':
                        reg_ids=self.pool.get('reglement.detail').search(cr, uid, [('invoice_id','=',facture.id),('reglement_id.date_reglement','>',date_debut)])
                        reg_objs = self.pool.get('reglement.detail').browse(cr, uid, reg_ids)
                        for reg in reg_objs:
	                        montant_reg+=reg.montant

                        fact_locaux+=montant_reg
                    else :
                        print"***************fact_locaux", fact_locaux
                        fact_locaux+=facture.reste_a_payer
                        print"***************fact_locaux2", fact_locaux

                    if facture.state=='ppaid':
                        print"***************fact_locaux3", fact_locaux

                        fact_locaux+=facture.reste_a_payer

            inv_picking_ids = self.pool.get('invoice.picking').search(cr, uid, [('date_invoice_picking','<=',date_debut),
                                                                                ('state','=','draft'),
                                                                                ('type','=','in_invoice'),
                                                                                ('currency_id','=','TND'),
                                                                                ('partner_id.name','!=','EPS')])
            inv_picking_objs = self.pool.get('invoice.picking').browse(cr, uid, inv_picking_ids)
            for inv_wiz in inv_picking_objs:
                print"***************amount_total_rep", inv_wiz.amount_total

            if inv_picking_objs:
                print"***************fact_locaux4", fact_locaux

                for inv_picking in inv_picking_objs  :
                    print"***************fact_locaux5", fact_locaux

                    fact_locaux+=inv_picking.amount_total
    # --------------------------------------------------------------------------------------------------------
##### créer par Maroua Romdhane		
	        ##### Stock
    # --------------------------------------------------------------------------------------------------------
#            stock=0
	        #####res['stock'] =stock
            #####cr.execute('SELECT * FROM product_product')
#            products_ids = self.pool.get('product.product').search(cr, uid, [])
#            products = self.pool.get('product.product').browse(cr, uid, products_ids)
#            quant_obj = self.pool.get("stock.quant")

#            for product in products:
#                dom = [('in_date', '<=', date_debut), ('location_id', 'child_of', 12), ('product_id','=', product.id)]
#                quants = quant_obj.search(cr, uid, dom)
#                tot_qty = 0
#                tot_qty_in = 0
#                tot_qty_out = 0
#                for quant in quant_obj.browse(cr, uid, quants, context=context):
#                    tot_qty_in += quant.qty

#                quants_out = quant_obj.search(cr, uid, [('in_date', '<=', date_debut), ('location_id', 'child_of', 9), ('product_id','=', product.id)])
#                for quant in quant_obj.browse(cr, uid, quants_out, context=context):
#                    tot_qty_out += quant.qty
#                tot_qty=tot_qty_in - tot_qty_out
#                if (tot_qty > 0 ):

#                    stock=stock+(product.purchase_price*tot_qty)
                
                    
                    
                #####stock=stock+(product.purchase_price*product.qty_available)
		        #####res['stock'] =stock
##### créer par Maroua Romdhane	
            	        

##### créer par Maroua TURKI	
	        ##### Stock
            stock=0
            products_ids = self.pool.get('product.product').search(cr, uid, [])
            products = self.pool.get('product.product').browse(cr, uid, products_ids)
            stock_objs = self.pool.get("stock.move")


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


                tot_qty=tot_qty_in - tot_qty_out
                if (tot_qty > 0 ):

                    stock=stock+(product.purchase_price*tot_qty)
#------------------------------------------------------------------------------------------------
#################### Créer par salwa ksila ; montant cheque depense
#------------------------------------------------------------------------------------------------
            cheque_dep = 0
            cheq_dep_ids = self.pool.get('office.cheque').search(cr, uid, [])
            cheq_objs = self.pool.get('office.cheque').browse(cr, uid, cheq_dep_ids)
            if cheq_objs:
                for cheq in cheq_objs:
                    if cheq.state == "encaisse":
                        if cheq.date_echance <= date_debut and cheq.date_encaissement > date_debut:
                            cheque_dep = cheque_dep + cheq.montant_monnaie_local
                    else:
                        if cheq.date_echance <= date_debut:
                            cheque_dep = cheque_dep + cheq.montant_monnaie_local



            # cheq_dep_ids = self.pool.get('office.cheque').search(cr, uid, [])
            # cheq_objs = self.pool.get('office.cheque').browse(cr, uid, cheq_dep_ids)
            # cheque_dep = 0

            # if cheq_objs:
            #     for cheq in cheq_objs:
            #         if cheq.date_echance <= date_debut or cheq.date_encaissement and date_debut < cheq.date_encaissement:
            #             cheque_dep = cheque_dep + cheq.montant_monnaie_local

#--------------------------------------------------------------------------------------------------
                        #cautions et grantie
###############updated by salwa ksila caution et garantie
#---------------------------------------------------------------------------------------------------
	       
            caution=0
            caution_ids = self.pool.get('office.caution').search(cr, uid, [])
            caution_objs = self.pool.get('office.caution').browse(cr, uid, caution_ids)
            
	        
            if caution_objs:
                for caut in caution_objs:
                    if caut.libere == False and caut.date_caution <= date_debut:
                        caution = caution + caut.montant

                    elif caut.libere and caut.date_liberation > date_debut and caut.date_caution <= date_debut:
                        caution = caution + caut.montant
                        # else :
                        # 	caution=caution+caut.montant
		        

        
            total=compte_biat+compte_zitouna+cheque_antidates+factures_clients+stock+solde_caisse+caution-(cheque_circ+fact_etrangr+fact_locaux+cheque_dep+avoir)
            ####fin  
            data={
                'compte_biat':compte_biat,
                'compte_zitouna':compte_zitouna,
                'cheque_antidates':cheque_antidates,
                'factures_clients':factures_clients,
                'solde_caisse':solde_caisse,
                'cheque_circ':cheque_circ,
                'fact_etrangr':fact_etrangr,
                'fact_locaux':fact_locaux,
                'stock':stock,
                'total':total,
                'cautions':caution,
                'avoir': avoir,
                'cheques': cheque_dep,
                'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",            
                         
            } 
            result.append(data)
                  
        return result

jasper_report.report_jasper('report.jasper_etat_profit_print', 'account.invoice', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
