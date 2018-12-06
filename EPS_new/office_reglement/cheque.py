# -*- coding: utf-8 -*-
import openerp.addons.decimal_precision as dp

from openerp import models, fields, api, exceptions



class OfficeCheque(models.Model):
    _name = 'office.cheque'
    _inherit = 'reglement.piece'

    name = fields.Char('Référence', readonly=True)
    titulaire = fields.Char(default="EPS")
    state = fields.Selection([
        ('draft', "Draft"),
        ('emis', "Emis"),
        ('encaisse', "Encaissed"),
    ])

    date_encaissement = fields.Date("Date Encaissement")
    # mode_reglement = fields.Selection([('cheque', 'Chèque'), ('trait', 'Trait'), ], default='cheque')
    date = fields.Date("Date d'écheance")

    @api.model
    def create(self, vals, ):
        vals['name'] = self.env['ir.sequence'].next_by_code('cheque.depense')
        new_id = super(OfficeCheque, self).create(vals)
        return new_id

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'emis'

    @api.multi
    def action_done(self):
        for r in self:
            if not r.date_encaissement:
                raise exceptions.ValidationError(("Date encaissement ne peut pas etre nul !"
                                                  "Veuillez saisir la date d'encaissement"))

        self.state = 'encaisse'



    # class OfficeCheque(osv.osv):
#
#     _name = 'office.cheque'
#     _inherit = 'reglement.piece'
#
#
#     _columns = {
#         'name' : fields.char('Référence', readonly=True ),
#         'num_cheque_traite': fields.char('N Cheque/Traite', states={'cashed': [('readonly', True)]}),
#         'date_echance': fields.date('Maturity Date', required=True, readonly=False,
#                                     states={'draft': [('readonly', False)]}),
#         'montant_piece': fields.float('Amount', digits_compute=dp.get_precision('Account'), readonly=True,
#                                       states={'draft': [('readonly', False)]}),
#         'partner_id': fields.many2one('res.partner', 'Partner', required=True, readonly=True,
#                                       states={'draft': [('readonly', False)]}),
#
#         'titulaire' : fields.char(default="EPS"),
#         'state' : fields.selection([
#             ('draft', "Draft"),
#             ('emis', "Emis"),
#             ('encaisse', "Encaissed"),
#         ]),
#
#         'date_encaissement' : fields.date("Date Encaissement"),
#         # mode_reglement = fields.Selection([('cheque', 'Chèque'), ('trait', 'Trait'), ], default='cheque')
#         'date': fields.date("Date d'écheance"),
#
# }
#
#
#     def action_draft(self, cr, uid, ids):
#         self.write(cr, uid, ids, {'state': 'draft'})
#         return True
#
#
#     def action_confirm(self, cr, uid, ids):
#         self.write(cr, uid, ids, {'state': 'emis'})
#         return True
#
#     def action_done(self, cr, uid, ids):
#
#         for id in ids:
#             date_encaiss = self.browse(cr, uid, id, ).date_encaissement
#             if not date_encaiss:
#                 raise osv.except_osv(("Date encaissement ne peut pas etre nul !"
#                                                               "Veuillez saisir la date d'encaissement"))
#         self.write(cr, uid, ids, {'state': 'encaisse'})
#         return True
#
#     def create(self, cr, uid, vals, context=None):
#         vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'cheque.depense')
#         res = super(OfficeCheque, self).create(cr, uid, vals, context)
#         return res
#
# OfficeCheque()

    # @api.model
    # def create(self, vals, ):
    #     vals['name'] = self.env['ir.sequence'].next_by_code('cheque.depense')
    #     new_id = super(OfficeCheque, self).create(vals)
    #     return new_id

    # @api.multi
    # def action_draft(self):
    #     self.state = 'draft'

    # @api.multi
    # def action_confirm(self):
    #     self.state = 'emis'

    # @api.multi
    # def action_done(self):
    #     for r in self:
    #         if not r.date_encaissement:
    #             raise exceptions.ValidationError(("Date encaissement ne peut pas etre nul !"
    #                                               "Veuillez saisir la date d'encaissement"))
    #
    #     self.state = 'encaisse'




















