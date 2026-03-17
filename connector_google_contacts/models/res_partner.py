from odoo import models, fields
from odoo.exceptions import UserError
import requests

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
### COJER LOS CONTACTOS DE GOOGLE CONTACTS Y CREAR LOS CONTACTOS EN ODOO
