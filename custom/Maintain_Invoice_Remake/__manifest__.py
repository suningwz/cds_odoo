# -*- coding: utf-8 -*-
{
    'name': 'Invoice Customer Remake',
    'version': '13.0.1.0',
    'category': '',
    'description': u"""
This module has been generated by Odoo Studio.
It contains the apps created with Studio and the customizations of existing apps.
""",
    'author': 'minhgroup',
    'depends': [
        'account', 'Maintain_Client', 'Maintain_Organization','inputmask_widget','Maintain_Bill_Schema','Maintain_Business_Partner_Group','Maintain_Business_Partners_Remake',
        'Maintain_Closing_Date','Maintain_Country_State','Maintain_Custom_Common','Maintain_Custom_Company_Office','Maintain_Custom_Create_Company','Maintain_Custom_Department',
        'Maintain_Custom_Department_Section','Maintain_Custom_Employee','Maintain_Custom_Search_Form','Maintain_Discount_Schema','Maintain_Freight_Category',
        'Maintain_Income_Payment','Maintain_Industry_Type','Maintain_Invoice_Print','Maintain_Organization','Maintain_Printer_Output',
        'Maintain_Product','Maintain_Product_Class','Maintain_Quotations','Maintain_Receipt_Divide','Maintain_Tax_Rate','Maintain_Widget_Sale_History','tgl_format_number'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_model_fields.xml',
        'data/ir_ui_view.xml',
        'data/sequence.xml',
        'views/add_js.xml',
        'views/account_payment_custom_view.xml',
#        'views/invoice_customer_custom_view.xml',
#         'views/report_invoice.xml',
#         'report/report_format1.xml',
#         'report/report_format2.xml',
#         'report/report_format3.xml',
#         'report/report_format4.xml',
#         'report/report_shipment1.xml'
    ],
    'qweb': [
        'static/src/xml/report_template.xml'
    ],
    'application': False,
    'license': 'OPL-1',
}
