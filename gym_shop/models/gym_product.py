from odoo import _, api, fields, models, tools

class Product(models.Model):
    _name = 'gym.product'

    shop_id = fields.Many2one('res.partner',domain=[('gym_account_type','=','shop')], required=True, default=lambda self: self.env.user.partner_id.id)
    name = fields.Char(required=True)
    price = fields.Float(required=True)

    url = fields.Char(string="URL")
    description = fields.Html()

    image = fields.Binary(string="Image", attachment=True)
    image_medium = fields.Binary(string="Image medium", attachment=True)
    image_small = fields.Binary(string="Image small", attachment=True)

    @api.model
    def create(self, vals):
        if vals.get("image"):
            tools.image_resize_images(vals, sizes={'image': (1024, None)})
        return super(Product, self).create(vals)
    
    @api.multi
    def write(self, vals):
        if vals.get("image"):
            tools.image_resize_images(vals, sizes={'image': (1024, None)}) 

        return super(Product, self).write(vals)
    