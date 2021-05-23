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
        'mail'
    ],
    'data': [
        'data/mail_template.xml',
        
        'security/res_groups.xml',

        'views/menus.xml',
        'views/res_partner_views.xml',
        'views/res_config_settings_views.xml',
        'views/templates.xml',

        'wizard/res_partner_change_pass_wizard.xml',
    ],
}