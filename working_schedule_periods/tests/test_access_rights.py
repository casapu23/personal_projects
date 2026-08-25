from odoo.exceptions import AccessError
from odoo.tests import tagged

from odoo.addons.working_schedule_periods.tests.common import TestWorkingSchedulePeriodsCommon

@tagged('post_install', '-at_install')
class TestAccessRights(TestWorkingSchedulePeriodsCommon):
    
    def test_regular_user_no_read_m2o_resource_calendar_period_id_in_hr(self):
        # with a regular user, make sure that it's not possible
        # to see the field 'resource_calendar_period_id' in hr.employee 
        limited_env = self.testing_employee.with_user(self.regular_user)
        
        with self.assertRaises(AccessError, msg="The user should not be able to read this field due to security restrictions."):
            limited_env.read(['resource_calendar_period_id'])
            
            
    def test_regular_user_no_read_working_schedule_period_menu_in_hr(self):
        # with a regular user, make sure that it's not possible
        # to see the menu 'menu_resource_calendar_period'      
        visible_menu_ids = self.env['ir.ui.menu'].with_user(
            self.regular_user
        )._visible_menu_ids()

        self.assertNotIn(
            self.working_schedule_period_menu.id,
            visible_menu_ids,
        )
        
        
        
    def test_user_read_m2o_resource_calendar_period_id_in_hr(self):
        # with a user, make sure that it's possible
        # to see the field 'resource_calendar_period_id' in hr.employee 
        user_env = self.testing_employee.with_user(self.resource_calendar_period_user)
        
        user_env.read(['resource_calendar_period_id'])

            
    def test_user_read_working_schedule_period_menu_in_hr(self):
        # with a user, make sure that it's possible
        # to see the menu 'menu_resource_calendar_period'      
        visible_menu_ids = self.env['ir.ui.menu'].with_user(
            self.resource_calendar_period_user
        )._visible_menu_ids()

        self.assertIn(
            self.working_schedule_period_menu.id,
            visible_menu_ids,
        )
        
        
        
    def test_admin_resource_calendar_period_id_crud(self):
        # with a admin, make sure that it's possible
        # to see the field 'resource_calendar_period_id' in hr.employee 
        admin_env = self.testing_employee.with_user(self.resource_calendar_period_admin)
        admin_env.read(['resource_calendar_period_id'])
        
        # furthermore, the admin can execute a crud in the model "resource.calendar.period"
        admin_env_model = self.resource_calendar_period_test.with_user(self.resource_calendar_period_admin)
        admin_env_model.read()
        admin_env_model.write({'name': 'testing'})
        created_period = admin_env_model.create({'name': 'testing create'})
        created_period.unlink()
            
    def test_admin_read_working_schedule_period_menu_in_hr(self):
        # with a admin, make sure that it's possible
        # to see the menu 'menu_resource_calendar_period'      
        visible_menu_ids = self.env['ir.ui.menu'].with_user(
            self.resource_calendar_period_admin
        )._visible_menu_ids()

        self.assertIn(
            self.working_schedule_period_menu.id,
            visible_menu_ids,
        )
