from odoo import _, api, fields, models

class DayOfWeek(models.Model):
    _name = 'gym.dayofweek'

    name = fields.Char(required=True, translate=True)
    abbreviation = fields.Char(required=True, translate=True)
    index = fields.Integer(required=True)

class WorkoutDayOfWeekRel:
    table = "gym_workout_dayofweek_rel"

    dayofweek_id = fields.Many2one('gym.dayofweek', required=True)
    workout_id = fields.Many2one('gym.workout', required=True)
    