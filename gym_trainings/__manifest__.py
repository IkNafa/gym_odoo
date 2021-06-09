{
    'name': 'Gym Trainings',
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
        'security/ir_model_access.xml',
        'security/ir_rule.xml',

        'views/menus.xml',
        'views/gym_exercise_views.xml',
        'views/gym_workout_views.xml',
        'views/gym_workout_exercise_views.xml',
        'views/gym_event_views.xml',
    ],
}