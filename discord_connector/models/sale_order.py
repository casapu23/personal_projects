from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    discord_rule_id = fields.Many2one('discord.rule')
    
    def action_confirm(self):
        super().action_confirm()
        
        return self.discord_rule_id.event == 'sale_confirmed'