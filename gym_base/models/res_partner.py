from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    gender = fields.Selection([('male','Male'),('female','Female'),('other','Other')], string="Gender")
    birthday = fields.Date(string="Birthday")
    age = fields.Integer(compute="_compute_age", string="Age")

    child_ids = fields.One2many(domain=[('active', '=', True),('is_company','=',False),('gym_account_type','=','trainer')])

    sponsor_id = fields.Many2one('res.partner', string="Sponsor", domain=[('active', '=', True),('is_company','=',True),('gym_account_type','=','shop')])
    sponsored_ids = fields.One2many('res.partner', 'sponsor_id', string="Sponsored", domain=[('active', '=', True),('is_company','=',False),('gym_account_type','=','trainer')])

    sponsor_code = fields.Char(string="Code")

    gym_account_type = fields.Selection([('client','Client'),('trainer','Trainer'),('club','Club'),('shop','Shop')])

    follower_ids = fields.Many2many('res.partner','res_partner_follow_rel', 'following_id', 'follower_id')
    following_ids = fields.Many2many('res.partner','res_partner_follow_rel', 'follower_id', 'following_id')

    club_ids = fields.Many2many('res.partner','res_partner_club_rel','member_id','club_id')
    member_ids = fields.Many2many('res.partner','res_partner_club_rel','club_id','member_id')

    trainer_ids = fields.Many2many('res.partner','res_partner_client_trainer_rel','trainer_id','client_id')
    client_ids = fields.Many2many('res.partner','res_partner_client_trainer_rel','client_id','trainer_id')

    android_token = fields.Char()

    is_self = fields.Boolean(compute="_compute_is_self")
    is_following = fields.Boolean(compute="_compute_is_following")
    is_follower = fields.Boolean(compute="_compute_is_follower")
    is_member = fields.Boolean(compute="_compute_is_member")
    is_my_trainer = fields.Boolean(compute="_compute_is_my_trainer")
    is_my_sponsor = fields.Boolean(compute="_compute_is_my_sponsor")
    is_my_club = fields.Boolean(compute="_compute_is_my_club")
    has_request = fields.Boolean(compute="_compute_has_request")

    follower_count = fields.Integer(compute="_compute_follower_count")
    following_count = fields.Integer(compute="_compute_following_count")
    member_count = fields.Integer(compute="_compute_member_count")

    @api.depends('birthday')
    def _compute_age(self):
        today = fields.date.today()
        for record in self:
            if record.birthday:
                record.age = today.year - record.birthday.year - ((today.month, today.day) < (record.birthday.month, record.birthday.day))

    def _compute_is_self(self):
        for record in self:
            record.is_self = record.id == self.env.user.partner_id.id or record.id == self.env.user.partner_id.parent_id.id
    
    def _compute_is_following(self):
        for record in self:
            record.is_following = self.env.user.partner_id.id in record.following_ids.ids
    
    def _compute_is_follower(self):
        for record in self:
            record.is_follower = self.env.user.partner_id.id in record.follower_ids.ids
    
    def _compute_is_member(self):
        for record in self:
            record.is_member = self.env.user.partner_id.id in record.member_ids.ids

    def _compute_follower_count(self):
        for record in self:
            record.follower_count = len(record.follower_ids)
    
    def _compute_following_count(self):
        for record in self:
            record.following_count = len(record.following_ids)
    
    def _compute_member_count(self):
        for record in self:
            record.member_count = len(record.member_ids)
    
    def _compute_is_my_trainer(self):
        for record in self:
            record.is_my_trainer = self.env.user.partner_id.id in record.client_ids.ids
    
    def _compute_is_my_sponsor(self):
        for record in self:
            record.is_my_sponsor = self.env.user.partner_id.id == record.sponsor_id.id

    def _compute_is_my_club(self):
        for record in self:
            record.is_my_club = self.env.user.partner_id.id == record.parent_id.id
    
    def _compute_has_request(self):
        for record in self:
            record.has_request = self.env['res.partner.request'].search_count([('from_id','=',self.env.user.partner_id.id),('to_id','=',self.id)]) > 0

    def send_pass_recovery_mail(self):
        template_id = self.env.ref('gym_base.password_recovery_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        
    def follow_partner(self):
        self.ensure_one()
        if not self.is_self:
            self.env.user.partner_id.write({
                'following_ids':[(4,self.id)]
            })

    def unfollow_partner(self):
        self.ensure_one()
        if not self.is_self:
            self.env.user.partner_id.write({
                'following_ids':[(3,self.id)]
            })
    
    def join_club(self):
        self.ensure_one()
        if not self.is_self:
            self.env.user.partner_id.write({
                'club_ids':[(4,self.id)]
            })
    
    def leave_club(self):
        self.ensure_one()
        if not self.is_self:
            self.env.user.partner_id.write({
                'club_ids':[(3,self.id)]
            })

    @api.model
    def open_my_profile(self):
        return {
            'name': "Profile",
            'view_mode': 'form',
            'res_model': 'res.partner',
            'type':'ir.actions.act_window',
            'res_id': self.env.user.partner_id.id,
            'target':'current',
            'view_id': self.env.ref('gym_base.res_partner_view_form').id
        }
    
    def open_change_pass_wizard(self):
        user_id = self.env['res.users'].search([('partner_id','=',self.id)],limit=1)
        if not user_id:
            raise ValidationError('This user is not associated to an account')
        return {
            'name': "Change password",
            'view_type':'form',
            'view_mode': 'form',
            'res_model': 'res.partner.change.pass.wizard',
            'type':'ir.actions.act_window',
            'target':'new',
            'context':{'default_user_id':user_id.id}
        }
    
    def open_follower_view(self):
        self.ensure_one()
        action = self.env.ref('gym_base.res_partner_action').read()[0]
        action['domain'] = [('id','in',self.follower_ids.ids)]
        return action

    def open_following_view(self):
        self.ensure_one()
        action = self.env.ref('gym_base.res_partner_action').read()[0]
        action['domain'] = [('id','in',self.following_ids.ids)]
        return action
    
    def open_member_view(self):
        self.ensure_one()
        action = self.env.ref('gym_base.res_partner_action').read()[0]
        action['domain'] = [('id','in',self.member_ids.ids)]
        return action

    @api.model
    def open_my_employees(self):
        partner_id = self.env.user.partner_id
        action = self.env.ref('gym_base.res_partner_action').read()[0]
        if partner_id.gym_account_type == "shop":
            action['domain'] = [('id','in',partner_id.sponsored_ids.ids)]
        elif partner_id.gym_account_type == "club":
            action['domain'] = [('id','in',partner_id.child_ids.ids)]
        else:
            return False
        return action
    
    @api.model
    def open_my_trainers(self):
        partner_id = self.env.user.partner_id
        action = self.env.ref('gym_base.res_partner_action').read()[0]
        action['domain'] = [('id','in',partner_id.trainer_ids.ids)]
        return action
    
    @api.model
    def open_my_clients(self):
        partner_id = self.env.user.partner_id
        action = self.env.ref('gym_base.res_partner_action').read()[0]
        if partner_id.gym_account_type == "trainer":
            action['domain'] = [('id','in',partner_id.client_ids.ids)]
        elif partner_id.gym_account_type == "club":
            client_ids = sum(list(map(lambda employee_id: employee_id.client_ids.ids,partner_id.child_ids)),[])
            action['domain'] = [('id','in',client_ids)]
        return action

    @api.depends('is_company', 'name', 'parent_id.name', 'type', 'company_name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = "@%s" % (self.env['res.users'].search([('partner_id','=',record.id)],limit=1).login or "-")
    
    def send_request(self):
        self.ensure_one()
        self.env['res.partner.request'].create({
            'date': fields.Datetime.now(),
            'from_id': self.env.user.partner_id.id,
            'to_id': self.id,
            'type': self.gym_account_type or False,
        })

class ResPartnerFollowRel:
    _table = "res_partner_follow_rel"

    follower_id = fields.Many2one('res.partner', required=True)
    following_id = fields.Many2one('res.partner', required=True)

class ResPartnerClubRel:
    _table = "res_partner_club_rel"

    member_id = fields.Many2one('res.partner', required=True)
    club_id = fields.Many2one('res.partner', required=True)

class ResPartnerClientTrainerRel:
    _table = "res_partner_client_trainer_rel"

    client_id = fields.Many2one('res.partner', required=True, domain=[('is_company','=',False)])
    trainer_id = fields.Many2one('res.partner', required=True, domain=[('is_company','=',False),('gym_account_type','=','trainer')])