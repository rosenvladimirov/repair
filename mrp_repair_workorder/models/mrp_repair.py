# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class Repair(models.Model):
    _inherit = 'mrp.repair'

    production_id = fields.Many2one('mrp.production', 'Production order')
    workorder_id = fields.Many2one('mrp.workorder', 'Work order')
    employee_id = fields.Many2one('hr.employee', string='Worker', readonly=True)
    repair_employee_id = fields.Many2one('hr.employee', string='Responsible Worker')
