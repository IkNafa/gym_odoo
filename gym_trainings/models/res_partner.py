from odoo import _, api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    saved_workout_ids = fields.Many2many('gym.workout','saved_workout_res_partner_rel','workout_id','partner_id')
    