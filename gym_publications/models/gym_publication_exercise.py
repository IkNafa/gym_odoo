from odoo import _, api, fields, models

class PublicationExercise(models.Model):
    _name = 'gym.publication.exercise'

    publication_id = fields.Many2one('gym.publication', required=True, ondelete="cascade")
    exercise_id = fields.Many2one('gym.exercise', required=True, ondelete="cascade")

    sequence = fields.Integer()

    name = fields.Char(related="exercise_id.name")
    image = fields.Binary(related="exercise_id.image")
    image_medium = fields.Binary(related="exercise_id.image_medium")
    external_video = fields.Char(related="exercise_id.external_video")
    description = fields.Text(related="exercise_id.description")

    set_ids = fields.One2many('gym.publication.exercise.set','publication_exercise_id', string="Sets")
    set_str = fields.Char(compute="_compute_set_str", string="Sets")

    @api.depends('set_ids')
    def _compute_set_str(self):
        for record in self:
            if len(record.set_ids) > 0:
                record.set_str = str(len(record.set_ids)) + " x " + "-".join(map(lambda set_id: str(set_id.reps), record.set_ids))
            else:
                record.set_str = False
    