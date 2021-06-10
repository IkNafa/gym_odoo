{
    'name': 'Gym Publications',
    'version': '1.0',
    'description': '',
    'summary': '',
    'author': 'Iker Nafarrate',
    'website': '',
    'license': 'LGPL-3',
    'category': 'Fitness',
    'depends': [
        'gym_weighings','gym_trainings'
    ],
    'data': [
        'security/ir_model_access.xml',
        'security/ir_rule.xml',

        'views/gym_publication_views.xml',
        'views/gym_publication_exercise_views.xml',
        'views/gym_weighing_views.xml',
        'views/gym_workout_views.xml',
    ],
}