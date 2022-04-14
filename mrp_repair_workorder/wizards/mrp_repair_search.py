# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _

import logging
logger = logging.getLogger(__name__)


class MrpRepairChoice(models.TransientModel):
    _name = 'mrp.repair.choice'
    _inherit = "barcodes.barcode_events_mixin"

    repair_id = fields.Many2one('mrp.repair', 'Repair order')

    def on_barcode_scanned(self, barcode):
        repair = self.env['mrp.repair'].search(['|', '|',
                                                 ('product_id.default_code', '=', barcode),
                                                 ('lot_id.name', 'ilike', barcode[1:]),
                                                 ('lot_id.ref', '=', barcode)], limit=1)
        if repair:
            self.repair_id = repair
            return
        message = "A product with a barcode %s sent from a production order is not found in the repair orders."
        return {'warning': {
            'title': _("I can't find the product to repair"),
            'message': message % {
                'barcode': barcode}
        }}

    @api.multi
    def choice_repair_order(self):
        for record in self:
            if record.repair_id:
                attachment_view = self.env.ref('mrp_repair.view_repair_order_form', False)
                return {
                    'name': _('Repair order'),
                    'res_model': 'mrp.repair',
                    'type': 'ir.actions.act_window',
                    'view_id': attachment_view.id,
                    # 'views': [(False, 'tree'), (attachment_view.id, 'form')],
                    'view_mode': 'form',
                    'view_type': 'form',
                    'res_id': record.repair_id.id,
                    'target': 'self',
                }
            return {'type': 'ir.actions.act_window_close'}
