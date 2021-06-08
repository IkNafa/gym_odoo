from odoo import _, api, fields, models, tools

class Food(models.Model):
    _name = 'gym.food'

    name = fields.Char(required=True)
    type_id = fields.Many2one('gym.food.type', ondelete="set null")
    brand = fields.Char()

    image = fields.Binary(string="Image", attachment=True)
    image_medium = fields.Binary(string="Image medium", attachment=True)
    image_small = fields.Binary(string="Image small", attachment=True)

    is_prepared = fields.Boolean(default=False)

    line_ids = fields.One2many('gym.food.ingredient.line','parent_id')
    line_str = fields.Text(compute="_compute_text")

    calories = fields.Integer(
        string="Calories (kcal/100g)",
        compute="_compute_calories",
        store=True
    )

    fats = fields.Float(
        string="Fats (g)",
        compute="_compute_fats",
        inverse="_set_field",
        store=True
    )

    saturated_fats = fields.Float(
        string="Saturate Fats (g)",
        compute="_compute_saturated_fats",
        inverse="_set_field",
        store=True
    )

    carbohydrates = fields.Float(
        string="Carbohydrates (g)",
        compute="_compute_carbohydrates",
        inverse="_set_field",
        store=True
    )

    sugars = fields.Float(
        string="Sugars (g)",
        compute="_compute_sugars",
        inverse="_set_field",
        store=True
    )

    dietary_fiber = fields.Float(
        string="Dietary Fiber (g)",
        compute="_compute_dietary_fiber",
        inverse="_set_field",
        store=True
    )

    proteins = fields.Float(
        string="Proteins (g)",
        compute="_compute_proteins",
        inverse="_set_field",
        store=True
    )

    @api.depends('fats','carbohydrates','dietary_fiber','proteins')
    def _compute_calories(self):
        for record in self:
            record.calories = round(record.fats * 9 + record.carbohydrates * 4 + record.dietary_fiber * 2 + record.proteins * 4)
    
    @api.depends('line_ids')
    def _compute_fats(self):
        for record in self:
            if record.is_prepared and record.line_ids:
                record.fats = sum(map(lambda line_id: line_id.food_id.fats * line_id.quantity / 100, record.line_ids))
    
    @api.depends('line_ids')
    def _compute_saturated_fats(self):
        for record in self:
            if record.is_prepared and record.line_ids:
                record.saturated_fats = sum(map(lambda line_id: line_id.food_id.saturated_fats * line_id.quantity / 100, record.line_ids))
    
    @api.depends('line_ids')
    def _compute_carbohydrates(self):
        for record in self:
            if record.is_prepared and record.line_ids:
                record.carbohydrates = sum(map(lambda line_id: line_id.food_id.carbohydrates * line_id.quantity / 100, record.line_ids))
    
    @api.depends('line_ids')
    def _compute_sugars(self):
        for record in self:
            if record.is_prepared and record.line_ids:
                record.sugars = sum(map(lambda line_id: line_id.food_id.sugars * line_id.quantity / 100, record.line_ids))
    
    @api.depends('line_ids')
    def _compute_proteins(self):
        for record in self:
            if record.is_prepared and record.line_ids:
                record.proteins = sum(map(lambda line_id: line_id.food_id.proteins * line_id.quantity / 100, record.line_ids))
    
    @api.depends('line_ids')
    def _compute_dietary_fiber(self):
        for record in self:
            if record.is_prepared and record.line_ids:
                record.dietary_fiber = sum(map(lambda line_id: line_id.food_id.dietary_fiber * line_id.quantity / 100, record.line_ids))
    
    def _set_field(self):
        pass

    @api.depends('line_ids')
    def _compute_text(self):
        for record in self:
            if record.line_ids:
                record.line_str = "\n".join(map(lambda line_id: line_id.food_id.name + " - " + str(line_id.quantity) + "g", record.line_ids))
            else:
                record.line_str = False

    @api.model
    def create(self, vals):
        if vals.get("image"):
            tools.image_resize_images(vals, sizes={'image': (1024, None)})
        
        return super(Food, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get("image"):
            tools.image_resize_images(vals, sizes={'image': (1024, None)}) 

        return super(Food, self).write(vals)


class FoodLine(models.Model):
    _name = 'gym.food.ingredient.line'

    parent_id = fields.Many2one('gym.food', ondelete="cascade")

    food_id = fields.Many2one('gym.food', required=True, domain=[('is_prepared','=',False)], ondelete="cascade")
    quantity = fields.Integer(required=True, string="Quantity (g)")

    