from odoo import _, api, fields, models

class PublicationComment(models.Model):
    _name = 'gym.publication.comment'

    publication_id = fields.Many2one('gym.publication', required=True)

    partner_id = fields.Many2one('res.partner', required=True, default=lambda self: self.env.user.partner_id.id)
    datetime = fields.Datetime(string="Date", default=fields.Datetime.now(), required=True)
    message = fields.Text(required=True)