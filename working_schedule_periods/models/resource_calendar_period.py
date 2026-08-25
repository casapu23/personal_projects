from odoo import fields, models

class ResourceCalendarPeriod(models.Model):
    
    _name = 'resource.calendar.period'
    _description = "Working schedules periods"
    
    name = fields.Char(string="Working schedule period name")
    period_line_ids = fields.One2many('resource.calendar.period.line', 'resource_calendar_period_id')
    company_id = fields.Many2one('res.company')
