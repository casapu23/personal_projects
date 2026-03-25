from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"
    
    product_low_stock_already_sent_discord = fields.Boolean()

    @api.model
    def action_cron_low_stock(self):
        link = self.env['ir.config_parameter'].sudo(
        ).get_param('discord.stock_channel_url')

        # WE SEARCH THE PRODUCTS (SELF WILL BE EMPTY, THAT'S WHY WE DO IT LIKE THIS)
        product_orders = self.env["stock.warehouse.orderpoint"].search([
            ("active", "=", True),
            ("product_low_stock_already_sent_discord", "=", False)
        ])
        # THEN, DUE TO THE FIELDS qty_on_hand IS COMPUTED, NOT STORED, WE MUST DO IT WITH A ".filtered()"
        low_stock = product_orders.filtered(
            lambda r: r.qty_on_hand < r.product_min_qty
        )

        for product in low_stock:
            response = requests.post(
                link, json={"content": f"Low stock of this product: {product.product_id.name}"},)
            product.product_low_stock_already_sent_discord = True

            if response.status_code == 204:
                _logger.info("Mensaje enviado con éxito")
            else:
                _logger.info(
                    f"Error al enviar: {response.status_code}, {response.text}")
