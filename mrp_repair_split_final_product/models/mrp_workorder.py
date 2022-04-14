# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re

from odoo import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    def _toggle_mark_repair(self):
        if self.use_many_from_one:
            return {}
        return super(MrpWorkorder, self)._toggle_mark_repair()

    @api.model
    def _post_record_production(self):
        if self.use_many_from_one and self.split_production_ids:
            for line in self.split_production_ids:
                # _logger.info("FINAL LOT %s == %s" % (self.final_lot_id, line.lot_id))
                if self.final_lot_id == line.lot_id and line.repair_order:
                    # _logger.info("SPLIT %s==%s" % (line.lot_id.name, self.final_lot_id.name))
                    self.move_line_ids.filtered(
                        lambda move_line: not move_line.done_move and move_line.product_id == self.product_id and move_line.lot_produced_id == self.final_lot_id).write({
                        'repair_order': line.repair_order,
                    })
        return super(MrpWorkorder, self)._post_record_production()

    def on_barcode_scanned(self, barcode):
        if self.use_many_from_one and self.mark_repair:
            picking_type_id = self.production_id.picking_type_id
            parsed_result = picking_type_id.barcode_nomenclature_id.parse_barcode(barcode)
            if parsed_result['type'] in ['lot']:
                lot = parsed_result['lot']
                code = parsed_result['code']
                for line in self.split_production_ids.filtered(lambda r: r.lot_id.name == lot):
                    line.repair_order = not line.repair_order
                return
        return super(MrpWorkorder, self).on_barcode_scanned(barcode)


class MrpProductionSplit(models.Model):
    _inherit = "mrp.production.split"

    repair_order = fields.Boolean('For repair')
