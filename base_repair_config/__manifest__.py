# Copyright 2021 - TODAY, Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Base Repair Config',
    'summary': """
        Provides general settings for the Repair App""",
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Escodoo, Odoo Community Association (OCA)',
    'maintainers': ['marcelsavegnago'],
    'images': ['static/description/banner.png'],
    'website': 'https://github.com/oca/manufacture',
    'depends': [
        'mrp_repair',
        'stock',
    ],
    'data': [
        'views/res_config_settings.xml',
    ]
}
