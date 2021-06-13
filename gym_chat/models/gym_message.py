from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import humanize

class Message(models.Model):
    _name = 'gym.message'
    _order = "datetime desc"
    
    datetime = fields.Datetime()
    datetime_relative_str = fields.Char(compute="_compute_datetime_relative_str")
    from_id = fields.Many2one('res.partner',required=True, default=lambda self: self.env.user.partner_id.id)
    from_name = fields.Char(related="from_id.name")
    to_id = fields.Many2one('res.partner',required=True)
    to_name = fields.Char(related="to_id.name")
    message = fields.Text(required=True)

    @api.constrains('to_id')
    def _constrains_to_id(self):
        for record in self:
            if record.to_id.id == record.from_id.id:
                raise ValidationError("You can not send a message to yourself")
    
    def _compute_datetime_relative_str(self):
        for record in self:
            td = fields.Datetime.now() - record.datetime
            days, hours, minutes, seconds = td.days, td.seconds // 3600, td.seconds // 60 % 60, td.seconds
            if days > 0:
                relative_str = str(days) + " " + _("day(s)")
            elif hours > 0:
                relative_str = str(hours) + " " + _("hour(s)")
            elif minutes > 0:
                relative_str = str(minutes) + " " + _("minute(s)")
            else:
                relative_str = str(seconds) + " " + _("second(s)")
            
            datetime_str = _("%s ago" % relative_str)

            record.datetime_relative_str = datetime_str
    
    @api.model
    def create(self, vals):
        vals['datetime'] = fields.Datetime.now()
        return super(Message, self).create(vals)