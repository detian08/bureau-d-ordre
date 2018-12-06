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
    "name": "Documents Alfresco",
    "version": "0.1",
    "author": "i-way",
    "website": "http://iway-tn.com/",
    "category": "",
    "depends": ['office_product','office_sale','office_invoice','office_warning_box'],
    "description": "Gestion des documents électroniques",
    "init_xml": ['views/alfresco_config_views.xml',
                 'views/download_wizard_view.xml',
                 'produit_document/document_produit_view.xml',
                 'produit_document/upload_wizard_view.xml',
                 'sale_document/document_sale_view.xml',
                 'sale_document/upload_wizard_view.xml',
                 'fournisseur_document/document_fournisseur_view.xml',
                 'fournisseur_document/upload_wizard_view.xml',

                 ],
    "demo_xml": [],
    "update_xml": [
                'security/security.xml',
                'security/ir.model.access.csv',
                   ],
    "test": ['tests/tests.yml'],
    "installable": True
}
