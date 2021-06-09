from odoo import _, api, fields, models

class WorkoutExersiceSet(models.Model):
    _name = 'gym.workout.exercise.set'

    workout_exercise_id = fields.Many2one('gym.workout.exercise.set', required=True, ondelete="cascade")

    sequence = fields.Integer()

    weight = fields.Float()
    reps = fields.Integer(required=True)
    work_time = fields.Float()
    rest_time = fields.Float()
    