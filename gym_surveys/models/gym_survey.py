from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import json

class Survey(models.Model):
    _name = 'gym.survey'

    partner_id = fields.Many2one('res.partner', required=True, default=lambda self: self.env.user.partner_id.id, domain=[('gym_account_type','=','trainer')], ondelete="cascade")
    client_id = fields.Many2one('res.partner', required=True, ondelete="set null")

    name = fields.Char(required=True)
    type = fields.Selection([('initial','Initial'),('daily','Daily')], required=True)

    question_ids = fields.One2many('gym.survey.question', 'survey_id', string="Questions")
    question_count = fields.Integer(compute="_compute_question_count")
    answer_count = fields.Integer(compute="_compute_answer_count", store=False)
    last_answer = fields.Datetime(compute="_compute_last_answer")

    question_json = fields.Text(compute="_compute_question_json")

    @api.depends('question_ids')
    def _compute_question_json(self):
        for record in self:
            questions = []
            for question_id in record.question_ids:
                questions.append({
                    'id': str(question_id.id),
                    'title': question_id.name,
                    'required': question_id.required,
                })
            record.question_json = json.dumps(questions)


    def _compute_answer_count(self):
        for record in self:
            record.answer_count = sum(map(lambda question_id: len(question_id.answer_ids), record.question_ids))

    def _compute_last_answer(self):
        for record in self:
            datetime = False
            for question_id in record.question_ids:
                for answer_id in question_id.answer_ids:
                    if datetime:
                        datetime = max(datetime, answer_id.datetime)
                    else:
                        datetime = answer_id.datetime
            record.last_answer = datetime
    
    @api.depends('question_ids')
    def _compute_question_count(self):
        for record in self:
            record.question_count = len(record.question_ids)

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        return {'domain': {'client_id': [('id','in',self.partner_id.client_ids.ids)]}}

    @api.constrains('type')
    def _constrains_type(self):
        if self.type and self.type == "initial" and self.env['gym.survey'].search_count([('id','!=',self.id),('partner_id','=',self.partner_id.id),('client_id','=', self.client_id.id)]) > 0:
            raise ValidationError(self.client_id.name + " already has a initial survey")
    
    def openAnswers(self):
        return {
            'name': self.name,
            'view_mode': 'tree',
            'res_model': 'gym.survey.question.answer',
            'type':'ir.actions.act_window',
            'target':'current',
            'view_ids':"[(5,0,0),(0,0,{'view_mode':'tree', 'view_id': ref('gym_survey_question_answer_all_view_tree')})]",
            'domain':[('question_id','in',self.question_ids.ids)],
            'context':{
                'group_by': 'datetime:day'
            }
        }
    
    @api.model
    def open_pending_surveys(self):
        partner_id = self.env.user.partner_id
        survey_ids = self.env['gym.survey'].search([('client_id','=',partner_id.id)])
        survey_ids = list(map(lambda survey_id: survey_id.id, filter(lambda survey_id: (survey_id.type == "initial" and survey_id.answer_count == 0) or (survey_id.type == "daily" and (not survey_id.last_answer or (survey_id.last_answer - fields.Datetime.now()).days > 0)),survey_ids)))
        return {
            'name': _("Surveys"),
            'view_mode': 'tree',
            'res_model': 'gym.survey',
            'type':'ir.actions.act_window',
            'target':'current',
            'view_ids':"[(5,0,0),(0,0,{'view_mode':'tree', 'view_id': ref('gym_survey.gym_survey_view_tree')})]",
            'domain':[('id','in',survey_ids)],
        }
    
    def open_question_wizard(self):
        return {
            'name': self.name,
            'view_mode': 'form',
            'res_model': 'gym.survey.answers.wizard',
            'type':'ir.actions.act_window',
            'target':'new',
            'context':{'default_survey_id':self.id}
        }