# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models

import logging

_logger = logging.getLogger(__name__)

class MrpRepairBatch(models.Model):
    _name = 'mrp.repair.batch'
    _description = 'The repair in batch many products'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', copy=False, required=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code('mrp.repair.batch'))
    product_id = fields.Many2one(
        'product.product', string='Product to Repair',
        readonly=True, required=True, states={'draft': [('readonly', False)]})
