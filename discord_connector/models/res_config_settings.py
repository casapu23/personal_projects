from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sales_channel_url = fields.Char(config_parameter='discord_connector.sales_channel_url')
    stock_channel_url = fields.Char(config_parameter='discord_connector.stock_channel_url')
    accounting_channel_url = fields.Char(config_parameter='discord_connector.accounting_channel_url')
    