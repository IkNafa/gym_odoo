from odoo import _, api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    weighing_ids = fields.One2many('gym.weighing','partner_id', string="Weighings")
    weighing_count = fields.Integer(compute="_compute_weighing_count")

    def _compute_weighing_count(self):
        for record in self:
            record.weighing_count = len(record.weighing_ids)
    
    def open_user_weighings(self):
        self.ensure_one()
        return {
            'name': "Weighings",
            'view_mode': 'tree,form',
            'res_model': 'gym.weighing',
            'type':'ir.actions.act_window',
            'target':'current',
            'domain':[('partner_id','=',self.id)],
            'context':{'default_partner_id': self.id}
        }