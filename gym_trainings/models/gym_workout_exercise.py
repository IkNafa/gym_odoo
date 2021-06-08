from odoo import _, api, fields, models

class WorkoutExercise(models.Model):
    _name = 'gym.workout.exercise'

    workout_id = fields.Many2one('gym.workout', required=True)
    exercise_id = fields.Many2one('gym.exercise', required=True)

    sequence = fields.Integer()

    name = fields.Char(related="exercise_id.name")
    image = fields.Binary(related="exercise_id.image")
    image_medium = fields.Binary(related="exercise_id.image_medium")
    external_video = fields.Char(related="exercise_id.external_video")
    description = fields.Text(related="exercise_id.description")

    set_ids = fields.One2many('gym.workout.exercise.set','workout_exercise_id', string="Sets")
    set_str = fields.Char(compute="_compute_set_str", string="Sets")

    @api.depends('set_ids')
    def _compute_set_str(self):
        for record in self:
            record.set_str = str(len(record.set_ids)) + " x " + "-".join(map(lambda set_id: str(set_id.reps), record.set_ids))  

