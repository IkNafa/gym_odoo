from odoo import _, api, fields, models

class Event(models.Model):
    _name = 'gym.event'

    date_start = fields.Date(required=True)
    date_stop = fields.Date(required=True)
    type = fields.Selection([], required=True)
    partner_id = fields.Many2one('res.partner', ondelete="cascade")

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id,"%s - %s" % (str(record.date_start), record.type)))
        return result
    

    @api.model
    def open_my_calendar(self):
        partner_id = self.env.user.partner_id
        return {
            'name': "Calendar",
            'view_mode': 'calendar',
            'res_model': 'gym.event',
            'type':'ir.actions.act_window',
            'target':'current',
            'domain':[('partner_id','=',partner_id.id)],
        }