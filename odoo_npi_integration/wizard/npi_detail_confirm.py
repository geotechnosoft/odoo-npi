from openerp import models, fields, api
from openerp.tools.translate import _


class npi_detail_confirm(models.TransientModel):
    _name = 'npi.detail.confirm'
    _description = 'Confirm NPI Details before saving'

    name = fields.Char('Name', readonly=True)
    phone = fields.Char('Phone', readonly=True)
    email = fields.Char('Email', readonly=True)
    fax = fields.Char('Fax', readonly=True)
    credential = fields.Char('Credential', readonly=True)
    doctor_npi = fields.Char('Doctor NPI', readonly=True)
    street = fields.Char('Street', readonly=True)
    street2 = fields.Char('Street2', readonly=True)
    zip = fields.Char('Zip', size=126, change_default=True, readonly=True)
    city = fields.Char('City', readonly=True)
    state_id = fields.Many2one("res.country.state", 'State', readonly=True)
    country_id = fields.Many2one('res.country', 'Country', readonly=True)
    is_company = fields.Boolean('Organizational Provider', readonly=True)
    npi_dict = fields.Text('NPI Dictionary', readonly=True)

    @api.one
    def update_record(self):
        ''' Function to write NPI Details to Partner '''
        context = self.env.context.copy()
        if not context:
            context = {}
        active_id = context.get('active_id')
        if active_id:
            vals = {
                'credential': self.credential,
                'name': self.name,
                'zip': self.zip,
                'fax': self.fax,
                'phone': self.phone,
                'city': self.city,
                'street2': self.street2,
                'street': self.street,
                'state_id': self.state_id.id,
                'country_id': self.country_id.id,
                'is_company': self.is_company
            }
            partner = self.env['res.partner'].browse(active_id)
            partner.write(vals)
            partner.message_post(body=_('NPI Details were fetched for %s') % (partner.doctor_npi),
                                 subject='NPI info updated')
        return True
