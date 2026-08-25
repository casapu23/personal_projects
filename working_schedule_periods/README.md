# Working Schedule Periods

Odoo does not natively support different working schedules depending on the time of year. This is a common requirement in Spain, where companies often use a winter schedule and a summer schedule.

Without an extension, these changes have to be maintained manually. That becomes especially tedious when the same adjustment must be applied across an entire company, and using a custom script for every change is not a practical solution.

This module introduces working schedule periods so seasonal schedules can be configured in Odoo and assigned to employees without repeatedly editing calendars by hand.

## Features

- Defines working schedule periods through the `resource.calendar.period` model.
- Supports seasonal schedules such as winter and summer working hours.
- Assigns a working schedule period to an employee.
- Provides separate user and administrator security groups.
- Supports multi-company access through a record rule.

## Access rights

- **User**: can read working schedule periods.
- **Administrator**: can read, create, edit, and delete working schedule periods.
- A period linked to a company is visible only when that company is among the user's allowed companies.
- A period without a company is visible to users who can read the model.

## Tests

Run the module tests with:

```bash
./odoo-bin --addons-path=addons,../enterprise,../personal_projects \
    -d <database> --test-enable --stop-after-init \
    -u working_schedule_periods --test-tags /working_schedule_periods
```
