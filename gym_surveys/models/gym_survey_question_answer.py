from odoo import _, api, fields, models

class SurveyQuestionAnswer(models.Model):
    _name = 'gym.survey.question.answer'
    _order = "datetime asc"

    question_id = fields.Many2one('gym.survey.question', required=True, ondelete="cascade")
    datetime = fields.Datetime()
    answer = fields.Text()

    @api.model
    def create(self, vals):
        vals['datetime'] = fields.Datetime.now()
        return super(SurveyQuestionAnswer, self).create(vals)