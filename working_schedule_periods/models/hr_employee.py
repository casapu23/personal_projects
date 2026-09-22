from odoo import fields, models, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    resource_calendar_period_id = fields.Many2one('resource.calendar.period', groups="working_schedule_periods.working_schedule_periods_group_user")


    def _update_employee_working_schedule_period(self):
        employees = self.env['hr.employee'].search([('resource_calendar_period_id', '!=', False)])
        now = fields.Datetime.now()

        for employee in employees:
            period = employee.resource_calendar_period_id
            if not period:
                continue
                
        for line in period.period_line_ids:
            if line.start_period <= now and line.end_period >= now:
                employee.resource_calendar_id = line.resource_calendar_id
                break

    @api.onchange('resource_calendar_period_id')
    def _onchange_resource_calendar_period_id(self):
        for i in self:
            if i.resource_calendar_period_id:
                period_lines = i.resource_calendar_period_id.period_line_ids
                for line in period_lines:
                    now = fields.Datetime.now()
                    if line.start_period <= now and line.end_period >= now:
                        i.resource_calendar_id = line.resource_calendar_id
    
    # due to the field "resource_calendar_id" it's updated through an onchange,
    # I wrote this small write if in the future the value must be read by an API or executed with an script
    def write(self, vals):
        result = super().write(vals)

        if 'resource_calendar_period_id' in vals:
            self._onchange_resource_calendar_period_id()

        return result

    def _cron_check_employee_working_schedule_period(self):
        return self._update_employee_working_schedule_period()
