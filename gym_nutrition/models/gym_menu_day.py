from odoo import _, api, fields, models

class MenuDay(models.Model):
    _name = 'gym.menu.day'
    _rec_name = "day_id"

    menu_id = fields.Many2one('gym.menu', required=True, ondelete="cascade")

    day_id = fields.Many2one('gym.dayofweek', string="Day of week", required=True)
    stage_ids = fields.One2many('gym.menu.day.stage','menu_day_id')
    
    stage_str = fields.Html(compute="_compute_stage_str")

    calories = fields.Integer(compute="_compute_calories")
    fats = fields.Float(compute="_compute_fats")
    carbohydrates = fields.Float(compute="_compute_carbohydrates")
    proteins = fields.Float(compute="_compute_proteins")

    @api.depends('stage_ids')
    def _compute_calories(self):
        for record in self:
            record.calories = sum(map(lambda stage_id: stage_id.calories, record.stage_ids))
    
    @api.depends('stage_ids')
    def _compute_fats(self):
        for record in self:
            record.fats = sum(map(lambda stage_id: stage_id.fats, record.stage_ids))
    
    @api.depends('stage_ids')
    def _compute_carbohydrates(self):
        for record in self:
            record.carbohydrates = sum(map(lambda stage_id: stage_id.carbohydrates, record.stage_ids))
    
    @api.depends('stage_ids')
    def _compute_proteins(self):
        for record in self:
            record.proteins = sum(map(lambda stage_id: stage_id.proteins, record.stage_ids))

    @api.depends('stage_ids')
    def _compute_stage_str(self):
        for record in self:
            stage_str = ""
            for stage_id in record.stage_ids:
                stage_str += stage_id.name + (stage_id.stage_line_str or "")
            
            record.stage_str = stage_str


