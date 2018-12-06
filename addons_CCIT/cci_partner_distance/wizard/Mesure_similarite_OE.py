# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.tools.translate import _
import time
from datetime import datetime,date
from pyjarowinkler import distance

class oe_mesure_similarite_oe(models.TransientModel):
    _name = "cci.wizard.mesure.similarite.oe"



    @api.one
    def to_search(self):
		oe_ids = self.env['res.partner'].search([])
		print 'oe_ids.....',oe_ids
		i=0
		j=0
		for oe_id in oe_ids:
			print 'oe_id.....',oe_id
			name_oe_id = self.env['res.partner'].browse(oe_id.id).name
			print 'name_oe_id.....',name_oe_id
			i=i+1
			
			for op_eco_id in oe_ids:
				print 'op_eco_id.....',op_eco_id
				name_op_eco_id = self.env['res.partner'].browse(op_eco_id.id).name
				print 'name_op_eco_id.....',name_op_eco_id
				val = distance.get_jaro_distance(name_oe_id, name_op_eco_id, winkler=False, scaling=0.1)
				print 'val.....',val
			        j=j+1
				print 'j.....',j
                        	if i==j :
					print 'i.....',i
					print ''
				else:
					if val > 0.9:
						vals = {
							'operator_id': oe_id.id,
							#'partner_id': self.id,
							'distance': val,  # give id of first
						}
						create_id = self.env['res.partner.distance'].create(vals)





oe_mesure_similarite_oe()


