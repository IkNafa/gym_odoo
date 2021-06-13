from odoo import _, api, fields, models
import json

class Publication(models.Model):
    _name = 'gym.publication'
    _rec_name = "title"
    _order="datetime desc"

    datetime = fields.Datetime(required=True, default=fields.Datetime.now())
    title = fields.Char(required=True)
    partner_id = fields.Many2one('res.partner', ondelete="cascade", default=lambda self: self.env.user.partner_id.id, required=True)
    type = fields.Selection([('weighing','WEIGHING'),('workout','WORKOUT')])

    club_id = fields.Many2one('res.partner', domain=[('is_company','=',True),('gym_account_type','=','club')])

    weighing_id = fields.Many2one('gym.weighing', ondelete="cascade")
    image = fields.Binary(related="weighing_id.image")
    weight = fields.Float(related="weighing_id.weight")
    height = fields.Float(related="weighing_id.height")
    measurement_method = fields.Selection(related="weighing_id.measurement_method")
    body_fat = fields.Float(string="Body Fat", related="weighing_id.body_fat")
    muscle_mass = fields.Float(string="Muscle Mass",related="weighing_id.muscle_mass")
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

    workout_id = fields.Many2one('gym.workout', ondelete="cascade")
    publication_exercise_ids = fields.One2many('gym.publication.exercise','publication_id')

    workout_partner_id = fields.Many2one(related="workout_id.partner_id", string="Created by")
    workout_client_id = fields.Many2one(related="workout_id.client_id")
    workout_exercise_ids = fields.One2many(related="workout_id.exercise_ids")

    comment_ids = fields.One2many('gym.publication.comment','publication_id', string="Comments")
    liked_partner_ids = fields.Many2many('res.partner', 'res_partner_publication_like_rel', 'partner_id', 'publication_id')

    liked_partner_count = fields.Integer(compute="_compute_liked_partner_count")
    has_like = fields.Boolean(compute="_compute_has_like")

    def _compute_has_like(self):
        partner_id = self.env.user.partner_id
        for record in self:
            record.has_like = partner_id.id in record.liked_partner_ids.ids
    
    @api.depends('liked_partner_ids')
    def _compute_liked_partner_count(self):
        for record in self:
            record.liked_partner_count = len(record.liked_partner_ids)

    def like(self):
        self.env.user.partner_id.write({
            'liked_publication_ids':[(4,self.id)]
        })
    
    def unlike(self):
        self.env.user.partner_id.write({
            'liked_publication_ids':[(3,self.id)]
        })
    
    def openLikedPartners(self):
        action = self.env.ref('gym_base.res_partner_action').read()[0]
        action["domain"] = [('id','in',self.liked_partner_ids.ids)]
        return action


    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for record in self:
            return {'domain': {'weighing_id': [('partner_id', '=', record.partner_id.id)], 'workout_id': ['|','|',('partner_id', '=', record.partner_id.id),('id','in',record.partner_id.saved_workout_ids.ids),('client_id','=',record.partner_id.id)]}}
    
    @api.model
    def create(self, vals):

        publication_id = super(Publication, self).create(vals)
        self.env['gym.event'].sudo().create({
            'date_start': publication_id.datetime,
            'date_stop': publication_id.datetime,
            'type':'publication',
            'publication_id': publication_id.id,
            'partner_id': publication_id.partner_id.id
        })
        return publication_id

class PartnerPublicationLikeRel:
    _table = "res_partner_publication_like_rel"

    partner_id = fields.Many2one('res.partner', required=True)
    publication_id = fields.Many2one('gym.publication', required=True)