from openerp import fields, models
from openerp.tools.translate import _
from openerp import api
from openerp.exceptions import Warning

import urllib2
import json


class ResPartner(models.Model):
    _inherit = 'res.partner'

    credential = fields.Char('Credential')
    doctor_npi = fields.Char('Doctor NPI', track_visibility='onchange')
    create_date = fields.Datetime('Create Date')

    @api.multi
    @api.onchange('doctor_npi')
    def onchange_doctor_npi(self):
        ''' Function to get npi details from https://npiregistry.cms.hhs.gov/ '''
        state_obj = self.env['res.country.state']
        country_obj = self.env['res.country']
        if not self:
            return
        if self.doctor_npi and not self.create_date:
            if len(self.doctor_npi) != 10:
                self.doctor_npi = ''
                warning = {
                    'title': _('Warning!'),
                    'message': _('Doctor NPI should be 10 digit!')
                }
                return {'warning': warning}
            url = "https://npiregistry.cms.hhs.gov/api/?number=%s" % self.doctor_npi
            request = urllib2.Request(url=url)
            f = urllib2.urlopen(request)
            result = json.loads(f.read())
            if not result.get('results', []):
                raise Warning(_('Warning'), _('No Doctor found for this NPI!'))
            for res in result.get('results', []):
                if res.get('basic', ''):
                    self.credential = res['basic'].get('credential', '')
                    name = str(res['basic'].get('first_name', '')).title()
                    if res['basic'].get('middle_name', ''):
                        name += ' ' + res['basic'].get('middle_name', '').title()
                    if res['basic'].get('last_name', ''):
                        name += ' ' + res['basic'].get('last_name', '').title()
                    self.name = name or ''
                    # For Organizational Providers
                    if res['enumeration_type'] and res[
                            'enumeration_type'] == 'NPI-2':
                        self.is_company = True
                        self.name = str(res['basic'].get('name', '')).title()
                for address in res.get('addresses', []):
                    if address.get('address_purpose', '') == 'MAILING':
                        self.street = address.get('address_1', '').title()
                        self.street2 = address.get('address_2', '').title()
                        self.city = address.get('city', '').title()
                        self.zip = address.get('postal_code', '')
                        self.fax = address.get('fax_number', '')
                        self.phone = address.get('telephone_number', '')
                        if address.get('state', ''):
                            state_ids = state_obj.search(
                                [('code', '=', address.get('state', ''))])
                            if state_ids:
                                self.state_id = state_ids[0].id
                                self.country_id = state_ids[0].country_id and state_ids[
                                    0].country_id.id or False
                        if address.get('country_code', ''):
                            country_ids = country_obj.search([('code', '=', address.get(
                                'country_code', ''))])
                            if country_ids:
                                self.country_id = country_ids[0].id
                    else:
                        continue

    @api.multi
    def get_npi_details(self):
        ''' Function to get npi details from https://npiregistry.cms.hhs.gov/ '''
        vals = {}
        state_obj = self.env['res.country.state']
        country_obj = self.env['res.country']
        if not self.doctor_npi:
            raise Warning(
                _('Warning'),
                _('There is no Doctor NPI for this doctor!'))
        if len(self.doctor_npi) != 10:
            raise Warning(_('Warning'), _('Doctor NPI should be 10 digit!'))
        url = "https://npiregistry.cms.hhs.gov/api/?number=%s" % self.doctor_npi
        request = urllib2.Request(url=url)
        f = urllib2.urlopen(request)
        result = json.loads(f.read())
        if 'results' not in result or not result.get('results', []):
            raise Warning(_('Warning'), _('No Doctor found for this NPI!'))
        for res in result.get('results', []):
            print res.get('basic', False)
            if res.get('basic', False):
                name = str(res['basic'].get('first_name', '')).title()
                if res['basic'].get('middle_name', ''):
                    name += ' ' + res['basic'].get('middle_name', '').title()
                if res['basic'].get('last_name', ''):
                    name += ' ' + res['basic'].get('last_name', '').title()
                vals = {
                    'credential': res['basic'].get('credential', ''),
                    'name': name or '',
                    'doctor_npi': self.doctor_npi
                }
                # For Organizational Providers
                if res.get('enumeration_type', '') == 'NPI-2':
                    vals.update({
                        'is_company': True,
                        'name': res['basic'].get('name', '')
                    })
                
            for address in res.get('addresses', []):
                if address.get('address_purpose', '') == 'MAILING':
                    vals.update(
                        {'street': address.get('address_1', '').title()})
                    vals.update(
                        {'street2': address.get('address_2', '').title()})
                    vals.update({'city': address.get('city', '').title()})
                    vals.update({'zip': address.get('postal_code', '')})
                    vals.update({'fax': address.get('fax_number', '')})
                    vals.update({'phone': address.get('telephone_number', '')})
                    if address.get('state', ''):
                        state_ids = state_obj.search(
                            [('code', '=', address.get('state', ''))])
                        if state_ids:
                            vals.update({'state_id': state_ids[0].id})
                            vals.update({'country_id': state_ids[0].country_id and state_ids[
                                0].country_id.id or False})
                    if 'country_id' not in vals and address.get(
                            'country_code', ''):
                        country_ids = country_obj.search([('code', '=', address.get(
                            'country_code', ''))])
                        if country_ids:
                            vals.update({'country_id': country_ids[0].id})
                else:
                    continue
        wiz_id = self.env['npi.detail.confirm'].create(vals)
        wiz_id.write({'npi_dict': vals})
        view_ref = self.env['ir.model.data'].get_object_reference(
            'odoo_npi_integration', 'npi_detail_confirm_form_view')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Confirm NPI Details'),
            'res_model': 'npi.detail.confirm',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_ref[1] if view_ref else False,
            'res_id': wiz_id.id,
            'target': 'new',
            'context': {'partner_id': self._ids[0]},
        }
