from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from datetime import timedelta

class Workout(models.Model):
    _name = 'gym.workout'

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today())
    end_date = fields.Date()
    description = fields.Text()

    partner_id = fields.Many2one('res.partner', domain=[('is_company','=',False)], required=True, default=lambda self: self.env.user.partner_id.id, ondelete="cascade")
    client_id = fields.Many2one('res.partner', domain=[('is_company','=',False)], ondelete="set null")

    is_trainer = fields.Boolean(compute="_compute_is_trainer")

    dayofweek_ids = fields.Many2many('gym.dayofweek', 'gym_workout_dayofweek_rel', 'dayofweek_id', 'workout_id')
    dayofweek_str = fields.Char(compute="_compute_dayofweek_str", string="Days of week")

    saved_partner_ids = fields.Many2many('res.partner','saved_workout_res_partner_rel','partner_id','workout_id')
    save = fields.Boolean()
    can_save = fields.Boolean(compute="_compute_can_save")
    is_saved = fields.Boolean(compute="_compute_is_saved")

    exercise_ids = fields.One2many('gym.workout.exercise','workout_id', string="Exercises")
    exercise_count = fields.Integer(compute="_compute_exercise_count")

    event_ids = fields.One2many('gym.event','workout_id')

    @api.depends('dayofweek_ids')
    def _compute_dayofweek_str(self):
        for record in self:
            record.dayofweek_str = "-".join(map(lambda dayofweek_id: dayofweek_id.abbreviation, record.dayofweek_ids))

    @api.depends('partner_id')
    def _compute_is_trainer(self):
        for record in self:
            if record.partner_id:
                record.is_trainer = record.partner_id.gym_account_type == "trainer"
    
    @api.depends('partner_id','client_id','save')
    def _compute_can_save(self):
        partner_id = self.env.user.partner_id
        for record in self:
            record.can_save = record.partner_id.id != partner_id.id and record.client_id.id != partner_id.id and record.save 
    
    def _compute_is_saved(self):
        partner_id = self.env.user.partner_id
        for record in self:
            record.is_saved = partner_id.id in record.saved_partner_ids.ids

    @api.depends('exercise_ids')  
    def _compute_exercise_count(self):
        for record in self:
            record.exercise_count = len(record.exercise_ids)
    
    @api.constrains('partner_id', 'client_id')
    def _constrains_fieldname(self):
        if self.client_id and self.partner_id.id == self.client_id.id:
            raise ValidationError('You cannot assign a workout to yourself')
    


    @api.model
    def open_my_workouts(self):
        partner_id = self.env.user.partner_id
        return {
            'name': "Workouts",
            'view_mode': 'kanban,tree,form',
            'res_model': 'gym.workout',
            'type':'ir.actions.act_window',
            'target':'current',
            'domain':['|','|',('partner_id','=',partner_id.id),('client_id','=',partner_id.id),('id','in',partner_id.saved_workout_ids.ids)],
        }
    
    
    def save_routine(self):
        self.ensure_one()
        self.env.user.partner_id.write({
            'saved_workout_ids': [(4,self.id)]
        })
    
    def remove_routine(self):
        self.ensure_one()
        self.env.user.partner_id.write({
            'saved_workout_ids': [(3,self.id)]
        })
    
    @api.model
    def create(self, vals):
        workout_id = super(Workout, self).create(vals)
        workout_id.create_events()
        return workout_id

    @api.multi
    def write(self, vals):
        if "save" in vals:
            if vals.get("save") == False:
                vals["saved_partner_ids"] = [5,0,0]
        return super(Workout, self).write(vals)

    def create_events(self):
        for record in self:
            if record.start_date and record.end_date:
                date = record.start_date
                next_index = min(map(lambda dayofweek_id:  (dayofweek_id.index - date.weekday()) % 7, record.dayofweek_ids))
                date += timedelta(days=next_index)
                while(date <= record.end_date):
                    #Crear
                    self.env['gym.event'].sudo().create({
                        'date_start': date,
                        'date_stop': date,
                        'type':'workout',
                        'workout_id': record.id,
                        'partner_id': record.partner_id.id
                    })

                    date += timedelta(days=1)
                    next_index = min(map(lambda dayofweek_id:  (dayofweek_id.index - date.weekday()) % 7, record.dayofweek_ids))
                    date += timedelta(days=next_index)


class SavedWorkoutResPartnerRel:
    _table = "saved_workout_res_partner_rel"

    workout_id = fields.Many2one('gym.workout', required=True)
    partner_id = fields.Many2one('res.partner', domain=[('is_company','=',False)])