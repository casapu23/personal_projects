from odoo import fields, models
import requests
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    discord_rule_id = fields.Many2one('discord.rule')
    
    discord_channel_id = fields.Many2one('discord.channel')
    
    def action_confirm(self):
        link = self.env['ir.config_parameter'].sudo().get_param('discord.sales_channel')
        
        response = requests.post(link, json={"content": f"✅ Pedido confirmado: {self.name}"},)
        
        if response.status_code == 204:
            _logger.info("Mensaje enviado con éxito")
        else:
            _logger.info(f"Error al enviar: {response.status_code}, {response.text}")
            

        
        return super().action_confirm()
