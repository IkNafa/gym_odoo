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

        def getPartnerImageURL(id):
            return "/web/image/ir.attachment/%s/datas " % str(self.env['ir.attachment'].search([('res_field','=','image_medium'),('res_id','=',id),('res_model','=','res.partner')],limit=1).id)

        message_ids = self.env['gym.message'].search([], order="datetime desc")
        res = []


        actual_partner_id = self.env.user.partner_id
        res_ids = []
        for message_id in message_ids:
            who_id = message_id.from_id if message_id.from_id.id != actual_partner_id.id else message_id.to_id
            if who_id.id not in res_ids:
                res.append({
                    'partner_id': who_id.id,
                    'name': who_id.name,
                    'relative_datetime': message_id.datetime_relative_str,
                    'message': message_id.message,
                    'mine': message_id.from_id.id == self.env.user.partner_id.id,
                    'image': getPartnerImageURL(who_id.id)
                })
                res_ids.append(who_id.id)

        partner_ids = self.env['res.partner'].search([('id','!=',self.env.user.partner_id.id),('id','not in',res_ids)])
        [res.append({
            'partner_id': partner_id.id,
            'name': partner_id.name,
            'image': getPartnerImageURL(partner_id.id),
            'message': ''
        }) for partner_id in partner_ids]
        return res

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
        
    