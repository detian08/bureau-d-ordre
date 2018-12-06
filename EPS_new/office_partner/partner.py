# -*- encoding: utf-8 -*-

from openerp import models, fields, api

from openerp.osv import fields, osv
from openerp import api
from openerp.tools.translate import _


# import netsvc
class res_partner(osv.osv):
    _name = "res.partner"
    _inherit = "res.partner"



    def _check_length(self, cr, uid, ids, context=None):
        for partner in self.browse(cr, uid, ids, context=context):
            if (len(self.browse(cr, uid, ids, context=context).name)) >= 80:
                return False

        return True



    _columns = {
        'reference': fields.char('Référence', select=1),
        'exoner': fields.boolean('Exonere'),
        'revendeur': fields.boolean('Revendeur'),
        'timbre': fields.boolean('Timbre'),
        'mf': fields.char('M.F', size=64),
        'code_tva': fields.char('Code TVA', size=32),
        'code_categ': fields.char('Code Categorie', size=32),
        'num_etab': fields.char('Num Etablissement', size=32),
        'property_account_receivable': fields.property(
            type='many2one',
            relation='account.account',
            string="Account Receivable",
            domain="[('type', '=', 'receivable')]",
            help="This account will be used instead of the default one as the receivable account for the current partner",
            required=True, default=None),
    }

    _constraints = [
        (_check_length, ' Nom du client trop long.', ['name'])
    ]

    def create(self, cr, uid, vals, context=None):
	if 'child_ids' in vals and vals['child_ids'] :

		vals['reference'] = self.pool.get('ir.sequence').get(cr, uid, 'partner.reference')

		# ---------------------------------trouver l'id du partenaire qu'on va créer------------------------------------
	cr.execute("SELECT MAX(id) FROM res_partner;")
	res = cr.fetchall()
	last_partner_id = res[0][0]
	new_partner_id = last_partner_id + 1

        if 'customer' in vals and vals['customer'] and (vals['use_parent_address']==False):

            # ---------------------Trouver le code du compte client le plus grand---------------------------------------
            cr.execute("SELECT MAX(CAST(code AS bigint))FROM account_account WHERE(code LIKE '411%' AND code ~ '^[0-9\.]+$')")
            res = cr.fetchall()
            last_customer_account_code = res[0][0]
            # ----------------------------------------------------------------------------------------------------------
            new_customer_account_code = last_customer_account_code + 1


            new_customer_account = self.pool.get('account.account').create(cr, uid,{'code': str(new_customer_account_code),'name': 'Client-' + vals['name'],'parent_id': 226, 'type': "receivable",'user_type': 2, 'active': True,'reconcile':True},context=context)



            new_property = self.pool.get('ir.property').create(cr, uid, {
                'value_reference': "account.account" + "," + str(new_customer_account),
                'res_id': "res.partner" + ',' + str(new_partner_id),
                'fields_id': 1957}, context=context)



        if 'supplier' in vals and vals['supplier'] and (vals['use_parent_address']==False):


            # ---------------------Trouver le code du compte fournisseur le plus grand-----------------------------
            cr.execute(
                "SELECT MAX(CAST(code AS bigint))FROM account_account WHERE(code LIKE '401%' AND code ~ '^[0-9\.]+$')")
            res = cr.fetchall()
            last_supplier_account_code = res[0][0]
            # ----------------------------------------------------------------------------------------------------------

            new_supplier_account_code = last_supplier_account_code + 1

            new_supplier_account = self.pool.get('account.account').create(cr, uid,
                                                                           {'code': str(new_supplier_account_code),
                                                                            'name': 'Frs-' + vals['name'],
                                                                            'parent_id': 206, 'type': "payable",
                                                                            'user_type': 3, 'active': True,
                                                                            'reconcile': True},
                                                                           context=context)

            new_property = self.pool.get('ir.property').create(cr, uid, {
                'value_reference': "account.account" + "," + str(new_supplier_account),
                'res_id': "res.partner" + ',' + str(new_partner_id),
                'fields_id': 1960} , context=context)

        return super(res_partner, self).create(cr, uid, vals, context)

   
    def unlink(self, cr, uid, ids, context=None):
        partner_id = self.browse(cr, uid, ids[0], context=context).id

        cr.execute("SELECT id FROM ir_property WHERE res_id LIKE '%" + str(partner_id) + "%'")
        res = cr.fetchall()

        properties_ids = []
        accounts_ids = []

        for i in range(len(res)):
            properties_ids.append(int(res[i][0]))

        cr.execute("SELECT SUBSTR(value_reference,17,10) FROM ir_property WHERE res_id LIKE '%" + str(partner_id) + "%'")
        res = cr.fetchall()

        for i in range(len(res)):
            accounts_ids.append(int(res[i][0]))

        # ----------------------------------------------------------------------

        #---------------------------------------------------------------------------------------------------------------


        self.pool.get('ir.property').unlink(cr, uid, properties_ids, context=None)

        self.pool.get('account.account').unlink(cr, uid, accounts_ids, context=None)

        res = super(res_partner, self).unlink(cr, uid, ids, context=context)
        return res

res_partner()
