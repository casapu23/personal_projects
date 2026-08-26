{
    'name': "Working schedule periods",
    'version': "19.0.1.0.0",
    'author': "casapu23",
    'license': "AGPL-3",
    'website': "https://github.com/casapu23/personal_projects",
    'category': "Employee",
    'depends': ["hr"],
    'data': [
        'views/resource_calendar_period_views.xml',
        'views/hr_employee_views.xml',
        'views/menuitems.xml',
        'security/ir.model.access.csv',
    ],
}
