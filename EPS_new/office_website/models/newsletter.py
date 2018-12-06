from openerp import models, fields, api


class office_newsletter(models.Model):
	_name = 'office.newsletter'

	email = fields.Char(string = "Email")
