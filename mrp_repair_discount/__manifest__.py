# Copyright 2015 Nicola Malcontenti - Agile Business Group
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Repair Discount",
    "version": "11.0.1.0.0",
    "category": "Manufacturing",
    "license": "AGPL-3",
    "author": "Rosen Vladimirov, BioPrint Ltd., "
              "Agile Business Group, "
              "Tecnativa, "
              "Odoo Community Association (OCA)",
    "website": "http://www.agilebg.com",
    'depends': [
        'mrp_repair'
    ],
    "data": ["views/mrp_repair_view.xml"],
    "installable": True,
}
