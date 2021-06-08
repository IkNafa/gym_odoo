{
    'name': 'G.Y.M: Get Your Moment',
    'version': '1.0',
    'description': '',
    'summary': '',
    'author': 'Iker Nafarrate',
    'website': 'http://getyourmoment.es',
    'license': 'LGPL-3',
    'category': 'Fitness',
    'depends': [
        'mail','snailmail'
    ],
    'data': [
        'data/gym_dayofweek.xml',
        'data/mail_template.xml',
        
        'security/res_groups.xml',
        'security/ir_model_access.xml',

        'views/menus.xml',
        'views/res_partner_views.xml',
        'views/res_config_settings_views.xml',
        'views/templates.xml',
        'views/gym_dayofweek_views.xml',
        'views/res_partner_request_views.xml',

        'wizard/res_partner_change_pass_wizard.xml',
    ],
}