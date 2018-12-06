# -*- coding: utf-8 -*-

from openerp.osv import fields, osv


class ResCompany(osv.Model):
    _inherit = "res.company"

    def _get_sps_account(self, cr, uid, ids, name, arg, context=None):
        Acquirer = self.pool['payment.acquirer']
        company_id = self.pool['res.users'].browse(cr, uid, uid, context=context).company_id.id
        sps_ids = Acquirer.search(cr, uid, [
            ('website_published', '=', True),
            ('name', 'ilike', 'sps'),
            ('company_id', '=', company_id),
        ], limit=1, context=context)
        if sps_ids:
            sps = Acquirer.browse(cr, uid, sps_ids[0], context=context)
            return dict.fromkeys(ids, sps.sps_email_account)
        return dict.fromkeys(ids, False)

    def _set_sps_account(self, cr, uid, id, name, value, arg, context=None):
        Acquirer = self.pool['payment.acquirer']
        company_id = self.pool['res.users'].browse(cr, uid, uid, context=context).company_id.id
        sps_account = self.browse(cr, uid, id, context=context).sps_account
        sps_ids = Acquirer.search(cr, uid, [
            ('website_published', '=', True),
            ('sps_email_account', '=', sps_account),
            ('company_id', '=', company_id),
        ], context=context)
        if sps_ids:
            Acquirer.write(cr, uid, sps_ids, {'sps_email_account': value}, context=context)
        return True

    _columns = {
        'sps_account': fields.function(
            _get_sps_account,
            fnct_inv=_set_sps_account,
            nodrop=True,
            type='char', string='sps Account',
            help="sps username (usually email) for receiving online payments."
        ),
    }
