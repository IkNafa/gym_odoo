from odoo import _, api, fields, models
from odoo.tools import pycompat
from odoo.tools.safe_eval import safe_eval

class MessageReport(models.TransientModel):
    _name = 'report.gym.message.report'

    def _get_html(self):
        result = {}
        rcontext = {}
        report = self.browse(self._context.get('active_id'))
        if report:
            rcontext['self'] = self
            result['html'] = self.env.ref(
                'gym_chat.'
                'report_gym_message_html').render(
                    rcontext)
        return result

    @api.model
    def get_html(self, given_context=None):
        return self.with_context(given_context)._get_html()
    
    @api.model
    def get_partner_ids(self):
        return list(dict.fromkeys(map(lambda message_id: message_id.from_id if message_id.from_id.id != self.env.user.partner_id.id else message_id.to_id, self.env['gym.message'].search([], order="datetime desc"))))

    def getMessages(self, partner_id):
        return self.env['gym.message'].search(['|',('to_id','=',partner_id.id),('from_id','=',partner_id.id)], order="datetime asc")

    def getLastMessage(self, partner_id):
        return self.env['gym.message'].search(['|',('to_id','=',partner_id.id),('from_id','=',partner_id.id)], order="datetime desc",limit=1)

    @api.model
    def button_export_html(self):

        action = self.env.ref(
            'gym_chat.'
            'action_gym_message_report_html')
        vals = action.read()[0]
        context1 = vals.get('context', {})
        if isinstance(context1, pycompat.string_types):
            context1 = safe_eval(context1)
        model = self.env['report.gym.message.report']
        report = model.create({})
        context1['active_id'] = report.id
        context1['active_ids'] = report.ids
        vals['context'] = context1
        return vals
        
    