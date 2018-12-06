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
#
{
    "name": "CONFIGURATION GROUPES",
    "version": "0.1",
    "author": "Marwa BEN MESSAOUD I-WAY",
    "website" : "http://www.iway-tn.com",
    "category": "Groups",
    "description": """
CONFIGURATION GROUPES.
========================
Ce module offre la gestion des groupes, pour nous permettre de gérer les droits d'accès de l’application.
On a défini trois groupes :\n
	\n* Groupe Gérant qui contiennent les gérants de l’application.
	\n* Groupe Responsable Vente qui gère la partie vente.
	\n* Groupe Responsable Achat qui gère la partie achat.
    \n* Groupe Responsable Marketing qui gère la partie marketing.""",




    "depends": ['base','account','purchase'],
    "data": ['security/office_groups.xml',

],
    "installable": True,


}
