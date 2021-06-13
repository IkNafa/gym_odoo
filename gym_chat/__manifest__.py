{
    'name': 'Gym Chat',
    'version': '1.0',
    'description': '',
    'summary': '',
    'author': 'Iker Nafarrate',
    'website': '',
    'license': 'LGPL-3',
    'category': 'Fitness',
    'depends': [
        'gym_base'
    ],
    'data': [
        'data/report_data.xml',

        'report/gym_message_report.xml',

        'security/ir_model_access.xml',
        'security/ir_rule.xml',

        'views/gym_message_views.xml',
    ],
    'demo': [
        ''
    ],
    'auto_install': True,
    'application': True,
}