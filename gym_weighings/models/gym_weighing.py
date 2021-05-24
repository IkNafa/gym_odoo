from odoo import _, api, fields, models

class Weighing(models.Model):
    _name = 'gym.weighing'
    _order = 'date desc'
    _rec_name = 'date'

    def _default_get_height(self):
        weighing_id = self.env['gym.weighing'].search([],limit=1,order="date desc")
        if weighing_id:
            return weighing_id.height
        return False

    partner_id = fields.Many2one('res.partner', required=True)

    # Basic data
    image = fields.Binary(string="Image", attachment=True)
    image_medium = fields.Binary(string="Image medium", attachment=True)
    image_small = fields.Binary(string="Image small", attachment=True)

    date = fields.Date(string="Date", required=True, default=fields.Date.today())
    weight = fields.Float(string="Weight", required=True)
    height = fields.Float(string="Height", required=True, default=lambda self: self._default_get_height())

    measurement_method = fields.Selection([('impedance','Impedance'),('inbody','InBody'),('fold','Skin Fold')], string="Measurement Method")

    # Impedance
    body_fat = fields.Float(string="Body Fat")
    muscle_mass = fields.Float(string="Muscle Mass")
    bmi = fields.Float(string="BMI")
    visceral_fat = fields.Float(string="Visceral Fat")
    basal_metabolism = fields.Float(string="Basal Metabolism")
    bone_mass = fields.Float(string="Bone Mass")
    water_percentage = fields.Float(string="Water Percentaje")
    proteins = fields.Float(string="Proteins")

    # InBody

    # Pliegues (Skin Fold)

    bicep_skinfold = fields.Float(string="Biceps")
    tricep_skinfold = fields.Float(string="Triceps")
    shoulder_skinfold = fields.Float(string="Shoulder")
    subillacres_skinfold = fields.Float(string="Subillacres")

    @api.model
    def open_my_progress(self):
        partner_id = self.env.user.partner_id
        return {
            'name': "Progress",
            'view_mode': 'graph',
            'res_model': 'gym.weighing',
            'type':'ir.actions.act_window',
            'target':'current',
            'domain':[('partner_id','=',partner_id.id)],
        }


    


    