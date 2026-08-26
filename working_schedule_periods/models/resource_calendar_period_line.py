from odoo import fields, models
import logging

_logger = logging.getLogger(__name__)

class ResourceCalendarPeriodLine(models.Model):

    _name = 'resource.calendar.period.line'
    _description = "Working schedules periods lines"
    
    name = fields.Char(string="Working schedule period name")
    start_period = fields.Datetime()
    end_period = fields.Datetime()
    resource_calendar_id = fields.Many2one('resource.calendar.period')
