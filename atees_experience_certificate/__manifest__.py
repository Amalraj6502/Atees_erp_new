# __manifest__.py
{
    'name': 'Atees Experience Certificate',
    'version': '17.0',
    'depends': ['base','hr'],
    'data': [

        'security/ir.model.access.csv',
        'security/group.xml',
        'security/relieve_form_rules.xml',
        'views/experience_form.xml',
        'views/relieve_form.xml',
        'data/sequence_data.xml',
        'report/action_experience.xml',
        'report/experience_certificate_template.xml',
        'report/relieve_report_action.xml',
        'report/relieve_report_template.xml',

    ],
    'installable': True,
    'application': True,
}
