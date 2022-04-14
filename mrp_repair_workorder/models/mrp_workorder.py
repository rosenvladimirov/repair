# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re

from odoo import api, fields, models, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    repair_id = fields.Many2one('mrp.repair', 'Repair order')
    internal_notes = fields.Text('Internal Notes')
    internal_notes_templates = fields.Many2one('base.comment.template', 'Note template')
    mark_repair = fields.Boolean('Mark for repair', help='Please checked it if for repair')

    def _toggle_mark_repair(self):
        final_move_ids = self.move_line_ids.filtered(
            lambda move_line: not move_line.done_move and not move_line.lot_produced_id and move_line.qty_done > 0)
        final_move_ids.write({
            'repair_order': self.mark_repair,
        })

    @api.multi
    def toggle_mark_repair(self):
        for record in self:
            record.mark_repair = not record.mark_repair
            record._toggle_mark_repair()

    @api.onchange('internal_notes_templates')
    def _onchange_internal_notes_templates(self):
        # _logger.info("TEST %s(%s)" % (self.internal_notes_templates, self._context))
        if self._context.get('internal_notes_templates'):
            self.update({
                'internal_notes_templates': self._context['internal_notes_templates']
            })
        if self.internal_notes_templates and self.internal_notes_templates.use:
            text = re.sub(re.compile('<.*?>'), '', self.internal_notes_templates.text)
            self.internal_notes = "%s %s" % (self.internal_notes, text + "\n")
        # _logger.info("TEST %s(%s)" % (self.internal_notes_templates, self._context))

    def on_barcode_scanned(self, barcode):
        picking_type_id = self.production_id.picking_type_id
        parsed_result = picking_type_id.barcode_nomenclature_id.parse_barcode(barcode)
        # _logger.info("PARCE RESULT %s" % parsed_result)

        if parsed_result['type'] in ['document']:
            code = parsed_result['code']
            template = self.env['base.comment.template'].search([('code', '=ilike', code[3:])])
            # _logger.info("TEMPLATE %s(%s)" % (template, code))
            if template and self.internal_notes_templates == template:
                self._onchange_internal_notes_templates()
                return
            elif template and self.internal_notes_templates != template:
                self.internal_notes_templates = template
                return
        return super(MrpWorkorder, self).on_barcode_scanned(barcode)

    def _repair_values(self, line):
        return {
            'production_id': self.production_id.id,
            'workorder_id': self.id,
            'product_id': self.product_id.id,
            'product_qty': self.qty_producing,
            'lot_id': self.final_lot_id.id,
            'product_uom': self.production_id.product_uom_id.id,
            'location_id': self.production_id.location_src_id.id,
            'location_dest_id': self.production_id.location_dest_id.id,
            'internal_notes': _('Order: %s-%s\n%s' % (self.name, self.production_id.name, self.internal_notes)),
            'employee_id': self.employee_id.id,
        }

    @api.model
    def _post_record_production(self):
        if self.mark_repair and not self.internal_notes:
            raise UserError('You try to mark Done product for repair without Note ...')
        final_move_ids = self.move_line_ids.filtered(
            lambda move_line: move_line.lot_produced_id == self.final_lot_id and move_line.repair_order)
        for line in final_move_ids:
            res = self.env['mrp.repair'].create(self._repair_values(line))
            if res:
                self.repair_id = res
                self.mark_repair = False
                self.internal_notes = False
                self.internal_notes_templates = False
        return super(MrpWorkorder, self)._post_record_production()


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    repair_order = fields.Boolean('For repair')
