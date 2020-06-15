# -*- coding: utf-8 -*-
{
    'name': "Bill Management",
    'summary': """Manage bill""",
    'description': """""",

    'author': "SKcompany",
    'website': "https://www.skcompany.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base_setup', 'Maintain_Custom_Department', 'Maintain_Custom_Department_Section',
        'Maintain_Custom_Employee', 'Maintain_Business_Partner_Group', 'Maintain_Closing_Date',
        'Maintain_Product_Class', 'Maintain_Product', 'Maintain_Freight_Category',
        'Maintain_Business_Partners_Remake', 'Maintain_Invoice_Remake',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/bill.xml',
        'views/menu_bill_management.xml',
    ],
    'qweb': [
        'static/src/xml/bill_advanced_search.xml',
        'static/src/xml/bill_product_lines.xml',
        'static/src/xml/create_bill_button.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}