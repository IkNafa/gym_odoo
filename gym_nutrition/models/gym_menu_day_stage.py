from odoo import _, api, fields, models

class Stage(models.Model):
    _name = 'gym.menu.day.stage'
    
    menu_day_id = fields.Many2one('gym.menu.day', required=True, ondelete="cascade")

    name = fields.Char(required=True)
    suggested_hour = fields.Float()

    stage_line_ids = fields.One2many('gym.menu.day.stage.line','stage_id', string="Stages")
    stage_line_str = fields.Html(compute="_compute_stage_line_str")

    calories = fields.Integer(compute="_compute_calories")
    fats = fields.Float(compute="_compute_fats")
    carbohydrates = fields.Float(compute="_compute_carbohydrates")
    proteins = fields.Float(compute="_compute_proteins")

    @api.depends('stage_line_ids')
    def _compute_calories(self):
        for record in self:
            record.calories = sum(map(lambda stage_line_id: stage_line_id.calories, record.stage_line_ids))
    
    @api.depends('stage_line_ids')
    def _compute_fats(self):
        for record in self:
            record.fats = sum(map(lambda stage_line_id: stage_line_id.fats, record.stage_line_ids))
    
    @api.depends('stage_line_ids')
    def _compute_carbohydrates(self):
        for record in self:
            record.carbohydrates = sum(map(lambda stage_line_id: stage_line_id.carbohydrates, record.stage_line_ids))
    
    @api.depends('stage_line_ids')
    def _compute_proteins(self):
        for record in self:
            record.proteins = sum(map(lambda stage_line_id: stage_line_id.proteins, record.stage_line_ids))
    
    @api.depends('stage_line_ids')
    def _compute_stage_line_str(self):
        for record in self:
            if record.stage_line_ids:
                record.stage_line_str = "<ul><li>" + "</li><li>".join(map(lambda line_id: line_id.food_id.name, record.stage_line_ids)) + "</li></ul>"
            else:
                record.stage_line_str = False
    
    def open_menu_day_stage_lines(self):
        return {
            'name': self.name,
            'view_mode': 'tree',
            'res_model': 'gym.menu.day.stage.line',
            'type':'ir.actions.act_window',
            'target':'new',
            'domain':[('stage_id','=',self.id)],
            'context':{'default_stage_id':self.id, 'form_view_initial_mode':'edit'}
        }

class StageLine(models.Model):
    _name = "gym.menu.day.stage.line"

    stage_id = fields.Many2one('gym.menu.day.stage', ondelete="cascade")
    food_id = fields.Many2one('gym.food', required=True, ondelete="cascade")
    quantity = fields.Integer(required=True, string="Quantity (g)")

    calories = fields.Integer(compute="_compute_calories")
    fats = fields.Float(compute="_compute_fats")
    carbohydrates = fields.Float(compute="_compute_carbohydrates")
    proteins = fields.Float(compute="_compute_proteins")

    @api.depends('food_id','quantity')
    def _compute_calories(self):
        for record in self:
            record.calories = record.food_id.calories * record.quantity / 100
    
    @api.depends('food_id','quantity')
    def _compute_fats(self):
        for record in self:
            record.fats = record.food_id.fats * record.quantity / 100
    
    @api.depends('food_id','quantity')
    def _compute_carbohydrates(self):
        for record in self:
            record.carbohydrates = record.food_id.carbohydrates * record.quantity / 100
    
    @api.depends('food_id','quantity')
    def _compute_proteins(self):
        for record in self:
            record.proteins = record.food_id.proteins * record.quantity / 100
    