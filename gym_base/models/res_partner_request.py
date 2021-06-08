from odoo import _, api, fields, models
import random
import string

class ResPartnerRequest(models.Model):
    _name = 'res.partner.request'
    
    type = fields.Selection([('trainer','Trainer'),('club','Employee'),('shop','Sponsor')])
    from_id = fields.Many2one('res.partner', required=True, string="From")
    to_id = fields.Many2one('res.partner',required=True, string="To")
    date = fields.Datetime(string="Date", required=True)

    def accept(self):
        self.ensure_one()

        if self.type == "trainer":
            self.to_id.write({
                'client_ids': [(4,self.from_id.id)]
            })
        elif self.type == "club":
            self.to_id.write({
                'child_ids': [(4,self.from_id.id)]
            })
        elif self.type == "shop":
            self.sudo().from_id.write({
                'sponsor_id': self.to_id.id,
                'sponsor_code': self.generate_sponsor_code()
            })

        self.unlink()
    
    def decline(self):
        self.unlink()

    @api.model
    def open_my_requests(self):
        return {
            'name': "My requests",
            'view_mode': 'tree',
            'res_model': 'res.partner.request',
            'type':'ir.actions.act_window',
            'target':'current',
            'domain':[('to_id','=',self.env.user.partner_id.id)]
        }
    
    def generate_sponsor_code(self):
        while True:
            code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
            if self.env['res.partner'].search_count([('sponsor_code','=',code)]) == 0:
                return code


    