from odoo.exceptions import AccessError
from odoo.tests import tagged

from odoo.addons.working_schedule_periods.tests.common import TestWorkingSchedulePeriodsCommon

@tagged('post_install', '-at_install')
class TestMultiCompany(TestWorkingSchedulePeriodsCommon):
        
    
    def test_read_working_schedule_period_active_company(self):
        # read a working schedule period with a company that the user has active
        period = self.resource_calendar_period_test_2.with_user(self.user_2)
                
        period.read(['name'])
        
            
    def test_read_working_schedule_period_unactive_company(self):
        # read a working schedule period with a company that the user hasn't active
        period = self.resource_calendar_period_test_2.with_user(self.user_1)
        
        with self.assertRaises(AccessError, msg="The user should not be able to read the working schedule period with the company 1"):
            period.read(['name'])
    
    def test_read_working_schedule_period_no_company(self):
        # read a working schedule period with no company
        period = self.resource_calendar_period_test_3.with_user(self.user_1)
                        
        period.read(['name'])
