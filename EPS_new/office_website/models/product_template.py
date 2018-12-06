import string
import re
from openerp.osv import osv, fields, expression
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp import api
from openerp.exceptions import ValidationError

class product_template(osv.osv):
    _inherit = 'product.template'

    _columns = {
        'price' : fields.float(string='Prix')
    }