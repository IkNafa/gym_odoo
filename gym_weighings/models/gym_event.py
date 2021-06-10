from odoo import _, api, fields, models

class Event(models.Model):
    _inherit = 'gym.event'

    type = fields.Selection(selection_add=[('weighing','WEIGHING')])
    weighing_id = fields.Many2one('gym.weighing', ondelete="cascade")

    weighing_image = fields.Binary(string="Image", related="weighing_id.image")
    weight = fields.Float(string="Weight", related="weighing_id.weight")
    height = fields.Float(string="Height", related="weighing_id.height")
    measurement_method = fields.Selection(string="Measurement Method", related="weighing_id.measurement_method")
    body_fat = fields.Float(string="Body Fat", related="weighing_id.body_fat")
    muscle_mass = fields.Float(string="Muscle Mass", related="weighing_id.muscle_mass")
    bmi = fields.Float(string="BMI", related="weighing_id.bmi")
    visceral_fat = fields.Float(string="Visceral Fat", related="weighing_id.visceral_fat")
    basal_metabolism = fields.Float(string="Basal Metabolism", related="weighing_id.basal_metabolism")
    bone_mass = fields.Float(string="Bone Mass", related="weighing_id.bone_mass")
    water_percentage = fields.Float(string="Water Percentaje", related="weighing_id.water_percentage")
    proteins = fields.Float(string="Proteins", related="weighing_id.proteins")
    bicep_skinfold = fields.Float(string="Biceps", related="weighing_id.bicep_skinfold")
    tricep_skinfold = fields.Float(string="Triceps", related="weighing_id.tricep_skinfold")
    shoulder_skinfold = fields.Float(string="Shoulder", related="weighing_id.shoulder_skinfold")
    subillacres_skinfold = fields.Float(string="Subillacres", related="weighing_id.subillacres_skinfold")
    
