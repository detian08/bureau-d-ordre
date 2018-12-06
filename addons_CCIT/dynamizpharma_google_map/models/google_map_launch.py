# -*- coding: utf-8 -*-
from openerp.tools.translate import _
from openerp import models, fields, api, exceptions, tools

class launch_map(models.Model):
    _inherit = "res.partner"

    @api.multi
    def open_map(self):
	print 'open map ........',self
        for partner in self:

            url="http://maps.google.com/maps?oi=map&q="
	    print 'url..................',url
            if partner.street:
                url+=partner.street.replace(' ','+')
            if partner.city:
                url+='+'+partner.city.replace(' ','+')
            if partner.state_id:
                url+='+'+partner.state_id.name.replace(' ','+')
            if partner.country_id:
                url+='+'+partner.country_id.name.replace(' ','+')
            if partner.zip:
                url+='+'+partner.zip.replace(' ','+')
	print 'enfin url..................',url
        return {'type':'ir.actions.act_url','target':'new','url':url}
