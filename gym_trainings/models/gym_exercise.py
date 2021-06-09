from odoo import _, api, fields, models, tools

class Exercise(models.Model):
    _name = 'gym.exercise'

    partner_id = fields.Many2one('res.partner', default=lambda self: self.env.user.partner_id.id, ondelete="cascade")

    name = fields.Char(string="Name", required=True, translate=True)
    description = fields.Text(string="Description")
    external_video = fields.Char(string="URL")

    image = fields.Binary(string="Image", attachment=True)
    image_medium = fields.Binary(string="Image medium", attachment=True)
    image_small = fields.Binary(string="Image small", attachment=True)

    state = fields.Selection([('private','Private'),('public','Public'),('base','Base')], string="State", default="private")

    def publish(self):
        self.ensure_one()
        self.write({
            'state':'public'
        })

    @api.model
    def create(self, vals):
        if vals.get("image"):
            tools.image_resize_images(vals, sizes={'image': (1024, None)})
        
        return super(Exercise, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get("image"):
            tools.image_resize_images(vals, sizes={'image': (1024, None)}) 

        return super(Exercise, self).write(vals)