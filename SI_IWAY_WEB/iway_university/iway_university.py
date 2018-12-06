# -*- coding: utf-8 -*-

from openerp.osv import osv
from openerp.osv import fields
import time


class category_establishment(osv.osv):
    """ Scolar establishment """
    _name = 'category.establishment'
    _description = 'Scolar Establishment'
    _columns = {
    'logo': fields.binary('Logo'),
    'name': fields.char('Nom', size=100, required=True),
    'abbreviation': fields.char('Abbreviation', size=10, required=True),
    'description': fields.text('Description'),
    'website': fields.char('Website', size=100),
    'address': fields.text('Address'),
    'establish_id' : fields.many2one('category.university', 'Université'),
    #'establishement_ids' : fields.one2many('category.university', 'university_id', 'Établissement'),
    }
    
    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []
        res=[]
        for u in self.browse(cr, uid, ids,context=context):
            res.append((u.id, u.name))
        return res

category_establishment()


class category_university(osv.osv):
    """ University """
    _name = 'category.university'
    _description = 'University'
    _table = 'category_university'
    _columns = {
    'logo': fields.binary('Logo'),
    'abbreviation': fields.char('Abbreviation', size=10, required=True),
    'name': fields.char('Nom', size=100, required=True),
    'description': fields.text('Description'),
    'website': fields.char('Website', size=100),
    'address': fields.text('Address'),
    'university_id' : fields.many2one('category.establishment', 'Université'),
    #'establishement_ids' : fields.one2many('category.university', 'university_id', 'Établissement'),
    #'university_ids' : fields.one2many('category.establishment', 'establish_id', 'Établissement'),
    'univer_id' : fields.one2many('category.establishment', 'establish_id','Etablissement'),
    }
    
    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []
        res=[]
        for u in self.browse(cr, uid, ids,context=context):
            res.append((u.id, u.abbreviation + ', ' + u.name))
        return res
    
category_university()

