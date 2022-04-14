# Copyright 2021 Rosen Vladimirov, BioPrint Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Mrp Repair Split Final Product',
    'summary': """
        Clue split final product with mrp repair work order""",
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Rosen Vladimirov, BioPrint Ltd.,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/manufacture',
    'depends': [
        'barcode_mrp_workorder',
        'mrp_repair_workorder',
        'mrp_split_final_product',
    ],
    'data': [
        'views/mrp_workorder_views.xml',
    ],
    'demo': [
    ],
}
