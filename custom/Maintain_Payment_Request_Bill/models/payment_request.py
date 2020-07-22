from odoo import fields, models
from custom.Maintain_Invoice_Remake.models.invoice_customer_custom import rounding


class PrintPaymentRequest(models.Model):
    _inherit = 'bill.invoice'

    last_billed_amount = fields.Monetary(string='Last Billed Amount', currency_field='currency_id')
    deposit_amount = fields.Monetary(string='Deposit Amount', currency_field='currency_id')
    balance_amount = fields.Monetary(string='Balance Amount', currency_field='currency_id')
    tax_amount = fields.Monetary(string='Tax Amount', currency_field='currency_id')
    customer_other_cd = fields.Char('Customer CD', readonly=True)
    invoices_number = fields.Integer(string='Number of Invoices', default=0)
    # con.

    bill_user_id = fields.Many2one('res.users', copy=False, tracking=True,
                                   string='Salesperson',
                                   default=lambda self: self.env.user)


class BillInvoiceDetail(models.Model):
    _inherit = 'bill.invoice.details'


class BillInfoGet(models.Model):
    _inherit = 'bill.info'

    def _get_customer_other_cd(self):
        for cd in self:
            # if self.partner_id:
            cd.customer_other_cd = cd.partner_id.customer_other_cd

    # その他CD
    customer_other_cd = fields.Char('Customer CD', readonly=True, compute='_get_customer_other_cd')

    def preview_invoice(self):
        return {
            'type': 'ir.actions.report',
            'report_name': 'Maintain_Payment_Request_Bill.reports',
            'model': 'bill.info',
            'report_type': "qweb-pdf",
        }

    def subtotal_amount_tax8(self):
        subtotal = 0
        for line in self.bill_detail_ids:
            if line.tax_rate == 8:
                subtotal += line.line_amount
        return subtotal

    def subtotal_amount_tax10(self):
        subtotal = 0
        for line in self.bill_detail_ids:
            if line.tax_rate == 10:
                subtotal += line.line_amount
        return subtotal

    def subtotal_amount_tax_o(self):
        subtotal = 0
        for line in self.bill_detail_ids:
            if line.tax_rate != 10 and line.tax_rate != 8:
                subtotal += line.line_amount
        return subtotal

    def amount_tax8(self):
        subtotal = 0
        for line in self.bill_detail_ids:
            if line.tax_rate == 8:
                if line.x_voucher_tax_transfer == 'foreign_tax':
                    subtotal += rounding(line.tax_amount, 0, line.account_move_line_id.move_id.customer_tax_rounding)
                elif line.x_voucher_tax_transfer == 'voucher':
                    subtotal += rounding(line.voucher_line_tax_amount, 2,
                                         line.account_move_line_id.move_id.customer_tax_rounding)
                elif line.x_voucher_tax_transfer == 'invoice':
                    subtotal += rounding(line.line_amount * line.tax_rate, 2,
                                         line.account_move_line_id.move_id.customer_tax_rounding)
        return rounding(subtotal, 0, self.partner_id.customer_tax_rounding)

    def amount_tax10(self):
        subtotal = 0
        for line in self.bill_detail_ids:
            if line.tax_rate == 10:
                if line.x_voucher_tax_transfer == 'foreign_tax':
                    subtotal += rounding(line.tax_amount, 0, line.account_move_line_id.move_id.customer_tax_rounding)
                elif line.x_voucher_tax_transfer == 'voucher':
                    subtotal += rounding(line.voucher_line_tax_amount, 2,
                                         line.account_move_line_id.move_id.customer_tax_rounding)
                elif line.x_voucher_tax_transfer == 'invoice':
                    subtotal += rounding(line.line_amount * line.tax_rate, 2,
                                         line.account_move_line_id.move_id.customer_tax_rounding)
        return rounding(subtotal, 0, self.partner_id.customer_tax_rounding)

    def amount_tax_o(self):
        subtotal = 0
        for re in self.bill_invoice_ids:
            for line in re.bill_invoice_details_ids:
                if line.tax_rate != 10 and line.tax_rate != 8:
                    if line.x_voucher_tax_transfer == 'foreign_tax':
                        subtotal += rounding(line.tax_amount, 0,
                                             line.account_move_line_id.move_id.customer_tax_rounding)
                    elif line.x_voucher_tax_transfer == 'voucher':
                        subtotal += rounding(line.voucher_line_tax_amount, 2,
                                             line.account_move_line_id.move_id.customer_tax_rounding)
                    elif line.x_voucher_tax_transfer == 'invoice':
                        subtotal += rounding(line.line_amount * line.tax_rate, 2,
                                             line.account_move_line_id.move_id.customer_tax_rounding)
            if line.x_voucher_tax_transfer == 'custom_tax':
                subtotal += re.amount_tax
        return rounding(subtotal, 0, self.partner_id.customer_tax_rounding)


class PartnerClass(models.Model):
    _inherit = 'res.partner'

    def set_supplier_name(self):
        for i in self:
            if i.group_supplier:
                i.group_supplier = i.customer_supplier_group_code.name

    group_supplier = fields.Char('set_supplier_name', compute='set_supplier_name')


class InvoiceClassCustom(models.Model):
    _inherit = 'account.move'

    # account_invoice_id
    payment_id = fields.One2many('account.payment', 'account_invoice_id')
    bill_invoice_ids = fields.One2many('bill.invoice', 'account_move_id')
