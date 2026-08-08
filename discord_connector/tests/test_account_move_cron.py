from odoo import fields
from odoo.tests import common, tagged
from odoo.exceptions import UserError
from unittest.mock import patch, MagicMock
from datetime import date, timedelta

@tagged('post_install', '-at_install')
class TestAccountMoveCron(common.TransactionCase):
    def setUp(self):
        super().setUp()
        
        self.partner = self.env["res.partner"].create({
            "name": "Test partner/company",
        })
        
        self.env['ir.config_parameter'].sudo().set_param(
            'discord_connector.accounting_channel_url',
            'https://discord.fake/webhook'
        )

    def _create_invoice(self, due_date, already_sent=False):
        invoice = self.env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": self.partner.id,
            "invoice_date": date.today() - timedelta(days=30),
            "invoice_date_due": due_date,
            "invoice_already_sent_discord": already_sent,
            "invoice_line_ids": [(0, 0, {
                "name": "Test product line",
                "quantity": 1,
                "price_unit": 100,
            })]
        })
        invoice.action_post()
        return invoice

    def test_expired_invoice_is_notified(self):
        invoice = self._create_invoice(due_date=date.today() - timedelta(days=1))

        mock_response = MagicMock()
        mock_response.status_code = 204

        with patch('requests.post', return_value=mock_response) as mock_post:
            self.env['account.move'].action_cron_expired_invoices()

            mock_post.assert_called_once()

            call_kwargs = mock_post.call_args
            self.assertIn(invoice.name, call_kwargs.kwargs['json']['content'])
            self.assertTrue(invoice.invoice_already_sent_discord)

    def test_already_sent_invoice_is_not_notified(self):
        invoice = self._create_invoice(
            due_date=date.today() - timedelta(days=1),
            already_sent=True
        )

        with patch('requests.post') as mock_post:
            self.env['account.move'].action_cron_expired_invoices()
            mock_post.assert_not_called()

    def test_not_expired_invoice_is_not_notified(self):
        invoice = self._create_invoice(due_date=date.today() + timedelta(days=10))

        with patch('requests.post') as mock_post:
            self.env['account.move'].action_cron_expired_invoices()
            mock_post.assert_not_called()
            self.assertFalse(invoice.invoice_already_sent_discord)

    def test_discord_error_does_not_mark_as_sent(self):
        invoice = self._create_invoice(due_date=date.today() - timedelta(days=1))

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"

        with patch('requests.post', return_value=mock_response):
            self.env['account.move'].action_cron_expired_invoices()
            self.assertFalse(invoice.invoice_already_sent_discord)

    def test_many_invoices_to_notify(self):
        invoices = [
            self._create_invoice(due_date=date.today() - timedelta(days=i))
            for i in range(1, 6)
        ]

        mock_response = MagicMock()
        mock_response.status_code = 204

        with patch('requests.post', return_value=mock_response) as mock_post:
            self.env['account.move'].action_cron_expired_invoices()
            self.assertEqual(mock_post.call_count, 5)

            for inv in invoices:
                self.assertTrue(inv.invoice_already_sent_discord)
