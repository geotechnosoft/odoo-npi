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
    'name': 'Odoo NPI Integration',
    'version': '1.0',
    'website': 'http://www.geotechnosoft.com',
    'summary': '',
    'description': """ This module integrates odoo with National Plan and Provider Enumeration System
        (NPPES) 'https://npiregistry.cms.hhs.gov'. This module fetches Doctor details from NPPES registry
        and fills in the partner form. NPI Details can be auto fetched while creating new doctor record
        in the system or old doctor can be refreshed with new information fetched from NPPES registry.
        For old records this module gives one level of verification for the information fetched from NPPES
        so, that information can be verified before writing into the doctor record as information in
        NPPES registry can be stale.
        
        """,
    'author': 'Geo Technosoft Pvt. Ltd',
    'depends': [
        'base'
    ],
    'data': [
        'wizard/npi_detail_confirm_view.xml',
        'res_partner_view.xml'
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
