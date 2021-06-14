from odoo import _, api, fields, models

class SurveyQuestion(models.Model):
    _name = 'gym.survey.question'

    survey_id = fields.Many2one('gym.survey', required=True, ondelete="cascade")
    name = fields.Char(required=True)
    required = fields.Boolean()

    answer_ids = fields.One2many('gym.survey.question.answer', 'question_id', string="Answers")
    