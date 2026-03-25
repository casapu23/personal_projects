from odoo import models, fields

class DiscordChannel(models.Model):
    _name = "discord.channel"
    
    def get_params_discord(self, channel):
        discord_dictionary_links = {}
        
        discord_sales_channel_url = self.env['ir.config_parameter'].sudo().get_param('discord.sales_channel')
        
        
        discord_dictionary_links.update("sales_channel", discord_sales_channel_url)
        
        return discord_dictionary_links
        