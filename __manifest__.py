{
    'name': 'Postfix Pipe Mail Integration',
    'version': '14.0.1.0.1',
    'category': 'Discuss',
    'summary': 'Custom mail integration for Postfix pipe setup',
    'description': '''
        Adds a "Postfix Pipe" server type to Incoming Email Servers
        allowing direct integration with Postfix pipe configurations.
        
        Features:
        - Custom server type: "Postfix Pipe"
        - Configurable script path
        - Direct mbox file processing
        - Maintains existing Postfix pipe setup
    ''',
    'author': 'Your Name',
    'website': 'https://dev.nomadic.net',
    'depends': ['fetchmail'],
    'data': [
        'views/fetchmail_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}