from odoo import _, api, fields, models

class Event(models.Model):
    _inherit = 'gym.event'

    type = fields.Selection(selection_add=[('workout','WORKOUT')])
    workout_id = fields.Many2one('gym.workout', ondelete="cascade")

    workout_name = fields.Char(related="workout_id.name")
    exercise_ids = fields.One2many(related="workout_id.exercise_ids")
    