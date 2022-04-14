# Copyright 2021 Rosen Vladimirov, BioPrint Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Mrp Repair and Work order',
    'summary': """
        Clue between mrp_repair and mrp. Added button in work order to mark current production for repair and 
        create repair order with data from work order.""",
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Rosen Vladimirov, BioPrint Ltd.,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/manufacture',
    'depends': [
        'mrp',
        'mrp_repair',
        'barcode_mrp_workorder',
        'barcodes',
        'base_comment_template',
        'hr',
        'mrp_workorder_manual',
    ],
    'data': [
        'views/mrp_workorder_views.xml',
        'views/repair_order.xml',
        'wizards/mrp_repair_search.xml',
    ],
    'demo': [
    ],
}
