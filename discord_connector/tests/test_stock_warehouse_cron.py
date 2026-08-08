from odoo.tests import common, tagged
from unittest.mock import patch, MagicMock
from datetime import date

@tagged('post_install', '-at_install')
class TestStockWarehouseOrderpointCron(common.TransactionCase):

    def setUp(self):
        super().setUp()

        self.env['ir.config_parameter'].sudo().set_param(
            'discord_connector.stock_channel_url',
            'https://discord.fake/webhook'
        )

        self.product = self.env['product.product'].create({
            "name": "Test Product",
            "is_storable": True,
        })

    def _create_orderpoint(self, qty_on_hand, product_min_qty, already_sent=False):
        orderpoint = self.env['stock.warehouse.orderpoint'].create({
            "product_id": self.product.id,
            "product_min_qty": product_min_qty,
            "product_max_qty": product_min_qty + 10,
            "product_low_stock_already_sent_discord": already_sent,
        })
        self.env['stock.quant'].create({
            "product_id": self.product.id,
            "location_id": self.env.ref('stock.stock_location_stock').id,
            "quantity": qty_on_hand,
        })
        return orderpoint

    def test_low_stock_is_notified(self):
        orderpoint = self._create_orderpoint(qty_on_hand=2, product_min_qty=10)

        mock_response = MagicMock()
        mock_response.status_code = 204

        with patch('requests.post', return_value=mock_response) as mock_post:
            self.env['stock.warehouse.orderpoint'].action_cron_low_stock()

            mock_post.assert_called_once()
            self.assertTrue(orderpoint.product_low_stock_already_sent_discord)

    def test_already_sent_is_not_notified(self):
        orderpoint = self._create_orderpoint(qty_on_hand=2, product_min_qty=10, already_sent=True)

        with patch('requests.post') as mock_post:
            self.env['stock.warehouse.orderpoint'].action_cron_low_stock()

            mock_post.assert_not_called()

    def test_sufficient_stock_is_not_notified(self):
        orderpoint = self._create_orderpoint(qty_on_hand=20, product_min_qty=10)

        with patch('requests.post') as mock_post:
            self.env['stock.warehouse.orderpoint'].action_cron_low_stock()

            mock_post.assert_not_called()
            self.assertFalse(orderpoint.product_low_stock_already_sent_discord)

    def test_discord_error_does_not_mark_as_sent(self):
        orderpoint = self._create_orderpoint(qty_on_hand=2, product_min_qty=10)

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"

        with patch('requests.post', return_value=mock_response):
            self.env['stock.warehouse.orderpoint'].action_cron_low_stock()

            self.assertFalse(orderpoint.product_low_stock_already_sent_discord)

    def test_many_low_stock_products_notified(self):
        products = [
            self.env['product.product'].create({
                "name": f"Product {i}",
                "is_storable": True,
            })
            for i in range(5)
        ]
        orderpoints = []
        for product in products:
            op = self.env['stock.warehouse.orderpoint'].create({
                "product_id": product.id,
                "product_min_qty": 10,
                "product_max_qty": 20,
            })
            self.env['stock.quant'].create({
                "product_id": product.id,
                "location_id": self.env.ref('stock.stock_location_stock').id,
                "quantity": 2,
            })
            orderpoints.append(op)

        mock_response = MagicMock()
        mock_response.status_code = 204

        with patch('requests.post', return_value=mock_response) as mock_post:
            self.env['stock.warehouse.orderpoint'].action_cron_low_stock()

            self.assertEqual(mock_post.call_count, 5)
            for op in orderpoints:
                self.assertTrue(op.product_low_stock_already_sent_discord)
