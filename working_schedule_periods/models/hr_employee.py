from odoo import fields, models
import logging

_logger = logging.getLogger(__name__)

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    use_calendar_periods = fields.Boolean()
    resource_calendar_period_id = fields.Many2one('resource.calendar.period')
    