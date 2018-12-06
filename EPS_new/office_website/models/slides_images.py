from openerp import models, fields, api


class slide_image(models.Model):
    _name = 'slide.image'
    _order = 'sequence, id DESC'

    name = fields.Char('Name')
    description = fields.Text('Description')
    sequence = fields.Integer('Sequence')
    image_alt = fields.Text('Image Label')
    image = fields.Binary('Image')
    image_small = fields.Binary('Small Image')
    #product_tmpl_id = fields.Many2one('product.template', 'Product', select=True)
    from_main_image = fields.Boolean('From Main Image', default=False)

