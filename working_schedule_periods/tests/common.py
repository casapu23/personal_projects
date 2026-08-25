from odoo.addons.mail.tests.common import mail_new_test_user
from odoo.tests import common

class TestWorkingSchedulePeriodsCommon(common.TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.company_test_1 = cls.env['res.company'].create({'name': 'Testing company'})
        cls.company_test_2 = cls.env['res.company'].create({'name': 'Testing company 2'})
        
        cls.regular_user = mail_new_test_user(
            cls.env,
            login='regular_user_1',
            groups='base.group_user,hr.group_hr_manager',
            company_id=cls.company_test_2.id,
        )
        cls.resource_calendar_period_user = mail_new_test_user(
            cls.env,
            login='resource_calendar_period_user_1',
            groups='base.group_user,hr.group_hr_manager,working_schedule_periods.working_schedule_periods_group_user',
            company_id=cls.company_test_1.id,
            company_ids=(cls.company_test_1 | cls.company_test_2).ids,
        )
        cls.resource_calendar_period_admin = mail_new_test_user(
            cls.env,
            login='resource_calendar_period_admin_1',
            groups='base.group_user,hr.group_hr_manager,working_schedule_periods.working_schedule_period_group_administrator',
            company_id=cls.company_test_1.id,
            company_ids=(cls.company_test_1 | cls.company_test_2).ids,
        )

        cls.user_1 = mail_new_test_user(
            cls.env,
            login='user_1',
            groups='base.group_user,hr.group_hr_manager,working_schedule_periods.working_schedule_periods_group_user',
            company_id=cls.company_test_1.id,
            company_ids=[cls.company_test_1.id],
        )
        cls.user_2 = mail_new_test_user(
            cls.env,
            login='user_2',
            groups='base.group_user,hr.group_hr_manager,working_schedule_periods.working_schedule_periods_group_user',
            company_id=cls.company_test_2.id,
            company_ids=[cls.company_test_2.id],
        )

        cls.resource_calendar_period_test = cls.env['resource.calendar.period'].create({
            'name': 'Working schedule period',
        })
        cls.resource_calendar_period_test_2 = cls.env['resource.calendar.period'].create({
            'name': 'Working schedule period 2',
            'company_id': cls.company_test_2.id,
        })
        cls.resource_calendar_period_test_3 = cls.env['resource.calendar.period'].create({
            'name': 'Working schedule period 3',
        })
        
        cls.testing_employee = cls.env['hr.employee'].create({
            'name': 'Jordi',
            'resource_calendar_period_id': cls.resource_calendar_period_test.id,
            'company_id': cls.company_test_1.id,
        })
        
        cls.working_schedule_period_menu = cls.env.ref('working_schedule_periods.menu_resource_calendar_period')
