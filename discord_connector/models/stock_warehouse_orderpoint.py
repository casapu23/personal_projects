from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    product_low_stock_already_sent_discord = fields.Boolean()

    def action_send_mail(self):
        template = self.env.ref("discord_connector.email_template_link_not_configured_stock")
        email_values = {'email_from': self.env.user.email}
        template.send_mail(self.id, force_send=True, email_values=email_values)

    @api.model
    def action_cron_low_stock(self):
        link = self.env['ir.config_parameter'].sudo().get_param(
            'discord_connector.stock_channel_url')
        _logger.info(f"Link for the stock discord channel {link}")
        if link == False or None:
            self.action_send_mail()
        else:
            # WE SEARCH THE PRODUCTS (SELF WILL BE EMPTY, THAT'S WHY WE DO IT LIKE THIS)
            product_orders = self.env["stock.warehouse.orderpoint"].search([
                ("active", "=", True),
                ("product_low_stock_already_sent_discord", "=", False)
            ])

            _logger.info(f"Regular products found: {product_orders}")

            # THEN, DUE TO THE FIELDS qty_on_hand IS COMPUTED, IT'S NOT STORED. THEN, WE MUST DO IT WITH A ".filtered()"
            low_stock = product_orders.filtered(
                lambda r: r.qty_on_hand < r.product_min_qty
            )

            _logger.info(f"Products with low stock: {low_stock}")

            for product in low_stock:
                response = requests.post(
                    link, json={"content": f"Low stock of this product: {product.product_id.name}. Actual stock: {product.qty_on_hand}. Minimun quantity we must have: {product.product_min_qty}."})
                product.product_low_stock_already_sent_discord = True

                if response.status_code == 204:
                    _logger.info(
                        f"Message sent with the low stock of the product: {product.product_id.name}")
                else:
                    _logger.info(
                        f"Sending error: {response.status_code}, {response.text}")
