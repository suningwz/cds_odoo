# -*- coding: utf-8 -*-
{
    'name': 'Quotations Custom',
    'version': '13.0',
    'author': 'BinhDT',
    'license': 'AGPL-3',
    'category': 'Extra Tools',
    'description': """
""",
    'depends': [
        'base_setup', 'sale_management', 'Maintain_Organization', 'Maintain_Client'
    ],
    'website': '',
    'depends': ['product', 'sale', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/add_js.xml',
        'views/quotations_custom_view.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False
}

