from odoo import fields
from odoo.tests import common, tagged
from odoo.exceptions import UserError
from unittest.mock import patch, MagicMock

@tagged('post_install', '-at_install')
class TestAccountMoveCron(common.TransactionCase):
    def setUp(self):
        super().setUp()
        # Aquí crearás los datos de prueba
        # Necesitas: una factura, un partner, configurar el parámetro del sistema
        # Pregunta: ¿cómo se crea un registro en Odoo dentro de un test?
        # Pista: self.env['account.move'].create({...})
        
        self.partner = self.env["res.partner"].create({
            "name": "Test partner/company",
            "id": 777
        })
        
        self.invoice = self.env["account.move"].create({
            "name": "INV/01",
            "partner_id": self.partner.id
        })

    def test_expired_invoice_is_notified(self):
        # 1. Crea una factura vencida
        # 2. Parchea requests.post
        # 3. Llama al cron
        # 4. Verifica con self.assertEqual / self.assertTrue
        pass

    def test_already_sent_invoice_is_not_notified(self):
        pass

    def test_not_expired_invoice_is_not_notified(self):
        pass

    def test_discord_error_does_not_mark_as_sent(self):
        pass
    
    def test_many_invoices_to_notify(self):
        pass