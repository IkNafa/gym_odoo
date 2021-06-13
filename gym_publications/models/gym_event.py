from odoo import _, api, fields, models

class Event(models.Model):
    _inherit = 'gym.event'

    type = fields.Selection(selection_add=[('publication','PUBLICATION')])
    publication_id = fields.Many2one('gym.publication', ondelete="cascade")

    publication_title = fields.Char(related="publication_id.title")
    