# -*- coding: utf-8 -*-
{
    'name': "My pet (+) - minhng.info",
    'summary': """My pet model""",
    'description': """Managing pet information""",
    'author': "minhng.info",
    'website': "https://minhng.info",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
        'product',
        'mypet'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/my_pet_plus_views.xml',
        # 'views/templates.xml',  # reference: https://www.odoo.com/documentation/14.0/developer/reference/javascript/javascript_reference.html
        # 'wizard/batch_update.xml',
        # 'views/res_config_settings_views.xml', # <-- add this

    ],
    # 'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': True,
}
