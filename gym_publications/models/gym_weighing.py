from odoo import _, api, fields, models

class Weighing(models.Model):
    _inherit = 'gym.weighing'

    def publish(self):
        return {
            'view_mode': 'form',
            'res_model': 'gym.publication',
            'type':'ir.actions.act_window',
            'target':'current',
            'context':{
                'form_view_initial_mode':'edit', 
                'default_weighing_id':self.id, 
                'default_type':'weighing'
            }
        }
    