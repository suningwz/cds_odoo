# -*- coding: utf-8 -*-
from odoo import models


class BillInfo(models.Model):
    _inherit = 'bill.info'

    def get_date(self):
        self.ensure_one()
        date = self.deadline.strftime('%Y年 %m月 %d日')
        print("====== date: ", date, type(date))
        return date
