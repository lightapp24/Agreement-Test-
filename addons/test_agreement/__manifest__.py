# -*- coding: utf-8 -*-

#  Copyright (c) 2023 Plotnikov S.E.
#  All rights reserved.
#

{
    'name': 'Agreement',
    'version': '1.0',
    'depends': [
        'base',
        'base_setup',
        'mail',
        'queue_job',
    ],
    'author': 'Plotnikov S.E.',
    'category': 'Uncategorized',
    'description': """
        This is test task module.
    """,
    'website': 'https://plotnikov24.ru/',
    'data': [
        'security/res.groups.csv',
        'security/ir.model.access.csv',
        'security/ir.rule.csv',
        'data/sequence.xml',
        'data/email_template.xml',
        'data/cron.xml',
        'views/menu.xml',
        'views/kind_agreement.xml',
        'views/agreement.xml',
    ],
    'installable': True,
    'application': True,
}
