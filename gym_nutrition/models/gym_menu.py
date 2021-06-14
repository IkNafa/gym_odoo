from odoo import _, api, fields, models

class Menu(models.Model):
    _name = 'gym.menu'
    
    name = fields.Char(required=True)
    start_date = fields.Date()
    end_date = fields.Date()

    is_trainer = fields.Boolean(compute="_compute_is_trainer")
    partner_id = fields.Many2one('res.partner', domain=[('is_company','=',False)], required=True)
    client_id = fields.Many2one('res.partner', domain=[('is_company','=',False)])

    menu_day_ids = fields.One2many('gym.menu.day','menu_id', string="Days")
    menu_day_count = fields.Integer(compute="_compute_menu_day_count")

    calories = fields.Integer(compute="_compute_calories")
    fats = fields.Float(compute="_compute_fats")
    carbohydrates = fields.Float(compute="_compute_carbohydrates")
    proteins = fields.Float(compute="_compute_proteins")

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for record in self:
            return {'domain': {'client_id': [('id', 'in', record.partner_id.client_ids.ids)]}}

    @api.depends('menu_day_ids')
    def _compute_calories(self):
        for record in self:
            record.calories = sum(map(lambda menu_day_id: menu_day_id.calories, record.menu_day_ids))
    
    @api.depends('menu_day_ids')
    def _compute_fats(self):
        for record in self:
            record.fats = sum(map(lambda menu_day_id: menu_day_id.fats, record.menu_day_ids))
    
    @api.depends('menu_day_ids')
    def _compute_carbohydrates(self):
        for record in self:
            record.carbohydrates = sum(map(lambda menu_day_id: menu_day_id.carbohydrates, record.menu_day_ids))
    
    @api.depends('menu_day_ids')
    def _compute_proteins(self):
        for record in self:
            record.proteins = sum(map(lambda menu_day_id: menu_day_id.proteins, record.menu_day_ids))

    @api.depends('menu_day_ids')
    def _compute_menu_day_count(self):
        for record in self:
            record.menu_day_count = len(record.menu_day_ids)

    @api.depends('partner_id')
    def _compute_is_trainer(self):
        for record in self:
            if record.partner_id:
                record.is_trainer = record.partner_id.gym_account_type == "trainer"
    
    @api.model
    def open_my_menus(self):
        partner_id = self.env.user.partner_id
        return {
            'name': "My Menus",
            'view_mode': 'tree,form',
            'res_model': 'gym.menu',
            'type':'ir.actions.act_window',
            'target':'current',
            'domain':['|',('partner_id','=',partner_id.id),('client_id','=',partner_id.id)],
            'context':{'default_partner_id':partner_id.id}
        }
    
    def open_menu_days(self):
        return {
            'name': "My Menus",
            'view_mode': 'tree,form',
            'res_model': 'gym.menu.day',
            'type':'ir.actions.act_window',
            'target':'current',
            'domain':[('menu_id','=',self.id)],
            'context':{'default_menu_id':self.id}
        }
    
    @api.model
    def create(self, vals):
        menu_id = super(Menu, self).create(vals)

        days = self.env['gym.dayofweek'].search([])
        menu_ids = []
        for day in days:
            menu_ids.append((0,0,{
                'menu_id': menu_id.id,
                'day_id': day.id
            }))
        menu_id.sudo().write({"menu_day_ids": menu_ids})

        return menu_id
    