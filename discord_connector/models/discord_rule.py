from odoo import models, fields
import requests
import logging

_logger = logging.getLogger(__name__)


class DiscordRule(models.Model):
    _name = "discord.rule"
    
    link = fields.Char()
    channel_id = fields.Many2one('discord.channel')
    event = fields.Selection(
        string="Types of event",
        selection=[
            ('sale_confirmed', 'Sale Confirmed'),
            ('low_stock', 'Low Stock'),
            ('invoice_expired', 'Invoice Expired'),
        ],
        compute='_compute_event',
        )
    
    def _compute_event(self):
        if self.event == 'sale_confirmed':
            link = self.channel_id.get_params_discord("sales_channel")
        
        response = requests.post(link, json="Hola test")
        
        if response.status_code == 204:
            _logger.info("Mensaje enviado con éxito")
        else:
            _logger.info(f"Error al enviar: {response.status_code}, {response.text}")
            
