from odoo import models, fields, api
from datetime import date, timedelta
import calendar


class BillingClass(models.Model):
    _inherit = 'res.partner'

    @staticmethod
    def _compute_closing_date(customer_closing_date):
        today = date.today()
        days_in_month = calendar.monthrange(today.year, today.month)[1]
        if today.month != 1:
            days_in_last_month = calendar.monthrange(today.year, today.month - 1)[1]
        else:
            days_in_last_month = calendar.monthrange(today.year - 1, 12)[1]
        _start = customer_closing_date.start_day
        _circle = customer_closing_date.closing_date_circle

        if today.day < _start:
            _current_closing_date = today.replace(day=_start) - timedelta(days=1)
            _last_closing_date = _current_closing_date - timedelta(days=days_in_last_month)
        else:
            _last_closing_date = today.replace(day=_start) - timedelta(days=1)
            _current_closing_date = _last_closing_date + timedelta(days=days_in_month)

        closing_date = {
            'last_closing_date': _last_closing_date,
            'current_closing_date': _current_closing_date,
        }

        return closing_date

    # Get invoices list by partner id
    def _get_invoices_by_partner_id(self, partner_id, last_closing_date, deadline):
        return self.env['account.move'].search([
            ('partner_id', 'in', partner_id),
            ('x_studio_date_invoiced', '>', last_closing_date),
            ('x_studio_date_invoiced', '<=', deadline),
            ('state', '=', 'posted'),
            ('type', '=', 'out_invoice'),
            ('bill_status', '!=', 'billed')
        ])

    def _compute_voucher_number(self, record):
        # Temporary variables are used to calculate voucher number
        number = 0

        # Get the records in the "res_partner" table with the same "請求先" as billing_code
        res_partner_id = self.env["res.partner"].search(
            ['|', ('customer_code', '=', record.customer_code), ('customer_code_bill', '=', record.customer_code)])

        # Calculate voucher number
        for rec in res_partner_id:
            number = number + len(self._get_invoices_by_partner_id(partner_id=rec.ids,
                                                                   last_closing_date=record.last_closing_date,
                                                                   deadline=record.deadline))
        return number

    @api.depends('customer_code', 'customer_code_bill')
    def _set_data_to_fields(self):
        for record in self:

            # Set data for last_closing_date field and deadline field
            if record.customer_closing_date:
                _closing_date = self._compute_closing_date(customer_closing_date=record.customer_closing_date)
                record.last_closing_date = _closing_date['last_closing_date']
                record.deadline = _closing_date['current_closing_date']

            # Set data for voucher_number field
            record.voucher_number = self._compute_voucher_number(record=record)

        return True

    @api.constrains('customer_code', 'customer_code_bill')
    def _check_billing_place(self):
        for record in self:
            # Customer has customer_code equal with customer_code_bill. This is a Billing Place
            if record.customer_code == record.customer_code_bill:
                record.is_billing_place = True
            else:
                record.is_billing_place = False

    # 前回締日
    last_closing_date = fields.Date(compute=_set_data_to_fields, readonly=True, store=False)

    # 締切日
    deadline = fields.Date(compute=_set_data_to_fields, readonly=True, store=False)

    # Voucher Number
    voucher_number = fields.Integer(compute=_set_data_to_fields, readonly=True, store=False)

    # Check customer is Billing Place
    is_billing_place = fields.Boolean(default=False)

    # Relational fields with account.move model
    account_move_ids = fields.One2many('account.move', 'billing_place_id', string='Invoices')

    # Button [抜粋/Excerpt]
    def bm_bill_excerpt_button(self):

        res_partner_id = self.env["res.partner"].search(
            ['|', ('customer_code', '=', self.customer_code), ('customer_code_bill', '=', self.customer_code)])

        self.account_move_ids = self._get_invoices_by_partner_id(partner_id=res_partner_id.ids,
                                                                 last_closing_date=self.last_closing_date,
                                                                 deadline=self.deadline)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Billing Details',
            'view_mode': 'tree,form',
            'res_model': 'res.partner',
            'res_id': self.id,
            'views': [(self.env.ref('Maintain_Bill_Management.bm_bill_form').id, 'form')],
        }

    # Action
    def action_bill(self):
        print(self.ids)
        print(self.ids)
        print(self.ids)
        print(self.ids)
        return True

    # Test button
    def test_buttonCC(self):
        print(self.account_move_ids)
        return True

    def get_lines(self):
        records = self.env['account.move.line'].search([
            ('move_id', 'in', self._ids),
            ('product_id', '!=', False)
        ]).read()

        # Get tax
        for record in records:
            if record['tax_ids']:
                self._cr.execute('''
                                            SELECT id, name
                                            FROM account_tax
                                            WHERE id IN %s
                                        ''', [tuple(record['tax_ids'])])
                query_res = self._cr.fetchall()
                record['tax_ids'] = ', '.join([str(res[1]) for res in query_res])

        return {
            'template': 'bill.product_lines',
            'records': records
        }

    def create_bill_for_invoice(self, argsSelectedData):
        for rec in argsSelectedData:
            res_partner_id = self.env["res.partner"].search(
                ['|', ('customer_code', '=', rec['customer_code']), ('customer_code_bill', '=', rec['customer_code'])])

            invoice_ids = self._get_invoices_by_partner_id(partner_id=res_partner_id.ids,
                                                           last_closing_date=rec['last_closing_date'],
                                                           deadline=rec['deadline'])
            invoice_ids.write({
                'bill_status': 'billed'
            })

            for invoice in invoice_ids:
                self.env['bill.header'].create({
                    'billing_code': rec['customer_code'],
                    'billing_name': rec['name'],
                    'last_closing_date': rec['last_closing_date'],
                    'deadline': rec['deadline'],
                    'partner_id': self.env["res.partner"].search([('id', '=', rec['id'])]).id,
                    'invoice_id': invoice.id,
                })

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }


class InvoiceClass(models.Model):
    _inherit = 'account.move'

    billing_place_id = fields.Many2one('res.partner')

    bill_status = fields.Char(default="not yet")
