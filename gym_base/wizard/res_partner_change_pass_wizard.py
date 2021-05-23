from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class ResPartnerChangePassWizard(models.TransientModel):
    _name = 'res.partner.change.pass.wizard'

    user_id = fields.Many2one('res.users', required=True)

    password = fields.Char(required=True, string="Password")
    rep_password = fields.Char(required=True, string="Repeat password")
    
    def change_password(self):
        self.ensure_one()
        if self.password != self.rep_password:
            raise ValidationError('Passwords must match')
        self.user_id.write({'password':self.password})
    