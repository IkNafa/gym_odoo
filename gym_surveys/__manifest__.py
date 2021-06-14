{
    'name': 'Gym Surveys',
    'version': '1.0',
    'description': '',
    'summary': '',
    'author': 'Iker Nafarrate',
    'website': '',
    'license': 'LGPL-3',
    'category': '',
    'depends': [
        'gym_base'
    ],
    'data': [
        'security/ir_model_access.xml',
        'security/ir_rule.xml',

        'views/assets_backend.xml',
        'views/gym_survey_views.xml',
        'views/gym_survey_question_answer_views.xml',

        'wizard/gym_survey_answers_wizard.xml',
    ],

    'qweb':[
        'static/src/xml/json_text_form_widget.xml'
    ],
}