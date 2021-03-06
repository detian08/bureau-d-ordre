# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
        "name" : "Product",
        "version" : "0.1",
        "author" : "WASSIM CHAABOUNI & Rim BEN DHAOU",
        "website" : "http://openerp.com",
        "category" : "Unknown",
        "description": """ Module Product """,
        "depends" : ['base','product','stock','account'],#'stock_location',],
        "init_xml" : [ ],
        "demo_xml" : [ ],
        "update_xml" : ['product_view.xml'],#,'ir_sequence.xml'],
        "installable": True,

}
