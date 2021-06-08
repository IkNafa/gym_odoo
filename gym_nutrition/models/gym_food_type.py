from odoo import _, api, fields, models

class FoodType(models.Model):
    _name = 'gym.food.type'

    name = fields.Char(required=True, translate=True)
    