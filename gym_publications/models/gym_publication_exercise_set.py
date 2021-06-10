from odoo import _, api, fields, models

class PublicationExerciseSet(models.Model):
    _name = 'gym.publication.exercise.set'

    publication_exercise_id = fields.Many2one('gym.publication.exercise.set', required=True, ondelete="cascade")

    sequence = fields.Integer()

    weight = fields.Float()
    reps = fields.Integer(required=True)
    work_time = fields.Float()
    rest_time = fields.Float()
    