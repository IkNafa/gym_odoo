from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    gender = fields.Selection([('male','Male'),('female','Female'),('other','Other')], string="Gender")
    birthday = fields.Date(string="Birthday")
    age = fields.Integer(compute="_compute_age", string="Age")

    gym_user_type = fields.Selection([('client','Client'),('trainer','Trainer')])
    gym_company_type = fields.Selection([('club','Club'),('shop','Shop')])

    follower_ids = fields.Many2many('res.partner','res_partner_follow_rel', 'following_id', 'follower_id')
    following_ids = fields.Many2many('res.partner','res_partner_follow_rel', 'follower_id', 'following_id')

    club_ids = fields.Many2many('res.partner','res_partner_club_rel','member_id','club_id')
    member_ids = fields.Many2many('res.partner','res_partner_club_rel','club_id','member_id')

    is_self = fields.Boolean(compute="_compute_is_self")
    is_following = fields.Boolean(compute="_compute_is_following")
    is_follower = fields.Boolean(compute="_compute_is_follower")
    is_member = fields.Boolean(compute="_compute_is_member")

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

    def send_pass_recovery_mail(self):
        template_id = self.env.ref('gym_base.password_recovery_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        
    def follow_partner(self):
        self.ensure_one()
        if not self.is_self:
            self.follower_ids = [(4,self.env.user.partner_id.id)]

    def unfollow_partner(self):
        self.ensure_one()
        if not self.is_self:
            self.follower_ids = [(3,self.env.user.partner_id.id)]
    
    def join_club(self):
        self.ensure_one()
        if not self.is_self:
            self.member_ids = [(4,self.env.user.partner_id.id)]
    
    def leave_club(self):
        self.ensure_one()
        if not self.is_self:
            self.member_ids = [(3,self.env.user.partner_id.id)]

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

    @api.depends('is_company', 'name', 'parent_id.name', 'type', 'company_name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = "@%s" % (self.env['res.users'].search([('partner_id','=',record.id)],limit=1).login or "-")
        


class ResPartnerFollowRel:
    _table = "res_partner_follow_rel"

    follower_id = fields.Many2one('res.partner', required=True)
    following_id = fields.Many2one('res.partner', required=True)

class ResPartnerClubRel:
    _table = "res_partner_club_rel"

    member_id = fields.Many2one('res.partner', required=True)
    club_id = fields.Many2one('res.partner', required=True)