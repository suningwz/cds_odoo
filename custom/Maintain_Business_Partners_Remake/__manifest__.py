# -*- coding: utf-8 -*-
{
    'name': 'Business Partner Customer Remake',
    'version': '13.0',
    'author': 'BinhDT',
    'license': 'AGPL-3',
    'category': 'Extra Tools',
    'description': """
""",
    'depends': [
        'base_setup', 'Maintain_Discount_Schema', 'Maintain_Invoice_Print', 'Maintain_Bill_Schema', 'account', 'Maintain_Business_Partner_Group', 'Maintain_Closing_Date'
    ],
    'website': '',
    'data': [
        'security/ir.model.access.csv',
        'views/add_js.xml',
        'views/partner_custom_view.xml',
        'views/sequence.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False
}
