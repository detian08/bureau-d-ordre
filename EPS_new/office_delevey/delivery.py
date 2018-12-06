from openerp.osv import fields, osv
from openerp import api

class res_partner(osv.osv):
    _inherit = 'res.partner'


    def _delivery_count(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for partner in self.browse(cr, uid, ids, context=context):
            res[partner.id] = len(partner.account_voucher_ids)
        return res


    _columns = {
            'voucher_count': fields.function(_delivery_count, string='# of Vouchers', type='integer'),
            'account_voucher_ids': fields.one2many('sale.devis', 'partner_id', 'Voucher History')

        }
