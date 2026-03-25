from odoo import fields, models, api
from datetime import timedelta, date
import requests
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"
        
    channel_id = fields.Many2one('discord.channel')
    
    invoice_already_sent_discord = fields.Boolean()
    
    @api.model
    def action_cron_expired_invoices(self):
        link = self.env['ir.config_parameter'].sudo().get_param('discord.account_channel')
        
        expired_invoices = self.env['account.move'].search([
            ("state", "=", "posted"),
            ("invoice_date_due", "<", fields.Date.today()),
            ("invoice_already_sent_discord", "=", False)
            ])
        
        
        
        for invoices in expired_invoices:
            response = requests.post(link, json={"content": f"Facturas vencidas: {invoices.name}"})
            invoices.invoice_already_sent_discord = True
    
            if response.status_code == 204:
                _logger.info("Mensaje enviado con éxito")
            else:
                _logger.info(f"Error al enviar: {response.status_code}, {response.text}")
