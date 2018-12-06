{
    'name': 'Stages',
    'category': 'Website',
    'version': '1.0',
    'summary': 'Job Descriptions And Application Forms',
    'description': """
OpenERP Contact Form
====================

        """,
    'author': 'OpenERP SA',
    'depends': ['website_partner', 'hr_recruitment', 'website_mail' ,'website_hr_recruitment'],
    'data': [
        #'security/ir.model.access.csv',
        #'security/website_hr_recruitment_security.xml',
        #'data/config_data.xml',
        'views/Iway_web.xml',
        #'views/templates.xml',
    ],
    'demo': [
        'data/hr_job_demo.xml',
    ],
    'installable': True,
}








