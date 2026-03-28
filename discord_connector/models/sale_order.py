from odoo import fields, models
import requests
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"
        
    def action_confirm(self):
        # SI CONFIRMO SIN UN LINK, DA ERROR: requests.exceptions.MissingSchema: Invalid URL 'False': No scheme supplied. Perhaps you meant https://False?
        link = self.env['ir.config_parameter'].sudo().get_param('discord_connector.sales_channel_url')
        _logger.info(f"Link for the sales discord channel {link}")
        
        response = requests.post(link, json={"content": f"The order {self.name} has been confirmed, total amount: {self.amount_total}{self.currency_id.symbol}"})
        
        if response.status_code == 204:
            _logger.info(f"Message sent with the order: {self.name}")
        else:
            _logger.info(f"Error al enviar: {response.status_code}, {response.text}")
        
        return super().action_confirm()
