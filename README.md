# Odoo Portfolio

This is my personal portfolio, sharing my ability and knowledge with everyone who wants!
All the modules included in this portfolio are designed for **Odoo Enterprise**.
---

## About me
I am a developer currently working with **Odoo 19**, with experience in:
- Developing custom modules.
- Customizing views (QWeb, XML).
- Automating business processes.
- Environment setup and deployments.

---

## Included projects

### [Private Contacts Access](./own_contacts/)
A custom security feature that restricts access to contacts in Odoo.
It can be installed in both environments: SaaS and SH.

### [Customer Discount Limit](./customer_discount_limit/)
A lightweight module that enforces a **maximum discount limit per customer** on sales orders.
It extends the `res.partner` model and integrates a validation in `sale.order.line` to ensure discounts do not exceed the configured limit.

### [Sale Cancellation Reason](./sale_cancel_reason/)
A module that enforces a **mandatory text explanation** when cancelling a Quotation or Sales Order.
It intercepts the standard cancel button, opens a Wizard for user input, and permanently saves the reason in the order history for audit purposes.

### [Discord Connector](./discord_connector/)
A module that connects Odoo with Discord to send real-time notifications for key business events.
It supports alerts for confirmed sales, low stock from reordering rules, and expired invoices, with webhook-based messaging and email fallback when the configuration is missing.

### [Odoo Scripts](./odoo_scripts/)
Collection of small, practical scripts for Odoo database and admin tasks.
Includes utilities and one-off SQL scripts (example: `adapt_currency_decimal`). Each script has its own README with usage, safety notes, and examples.

---

## Disclaimer / Warning
- The code in this repository is provided as examples to demonstrate my work and is not guaranteed to be production-ready.
- Each user is responsible for reviewing, testing, and adapting the code before using it.  
- I am not responsible for any consequences if third parties run these scripts or modules in their environments.