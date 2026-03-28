from odoo import fields, models, api
from datetime import timedelta, date
import requests
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"
            
    invoice_already_sent_discord = fields.Boolean()
    
    @api.model
    def action_cron_expired_invoices(self):
        link = self.env['ir.config_parameter'].sudo().get_param('discord_connector.accounting_channel_url')
        
        _logger.info(f"Link for the accounting discord channel {link}")
        
        expired_invoices = self.env['account.move'].search([
            ("state", "=", "posted"),
            ("invoice_date_due", "<", fields.Date.today()),
            ("invoice_already_sent_discord", "=", False),
            ])
        
        _logger.info(f"Expired invoices found: {expired_invoices.ids}")
        
        
        for invoices in expired_invoices:
            response = requests.post(link, json={"content": f"Expired invoice: {invoices.name} due on {invoices.invoice_date_due}."})
            invoices.invoice_already_sent_discord = True
    
            if response.status_code == 204:
                _logger.info(f"Message sent with the invoice: {invoices.name}")
            else:
                _logger.info(f"Error al enviar: {response.status_code}, {response.text}")
