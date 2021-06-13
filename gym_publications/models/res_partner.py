from odoo import _, api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    liked_publication_ids = fields.Many2many('gym.publication','res_partner_publication_like_rel','publication_id','partner_id')
    