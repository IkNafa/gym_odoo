from odoo import _, api, fields, models

class SurveyAnswersWizard(models.TransientModel):
    _name = 'gym.survey.answers.wizard'

    survey_id = fields.Many2one('gym.survey', required=True)
    question_json = fields.Text(related="survey_id.question_json")