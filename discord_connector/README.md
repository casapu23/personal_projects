# Discord Connector

A small Odoo module that sends notifications to Discord channels for Sales, Stock, and Accounting events.

## Features

- Sales
  - Sends a message when a sale order is confirmed.
- Stock
  - Sends a low-stock notification from `stock.warehouse.orderpoint` via scheduled cron.
- Accounting
  - Sends a notification when an invoice is expired via scheduled cron.
- Email fallback
  - If a Discord webhook URL is not configured, the module sends an email warning instead.

## Supported models

- `account.move` — expired invoice notifications
- `stock.warehouse.orderpoint` — low stock notifications
- `sale.order` — sales confirmation notifications
- `res.config.settings` — configuration of Discord webhook URLs

## Configuration

Go to `Settings` → `Discord Connector` and configure:

- `Discord Sales Channel URL`
- `Discord Stock Channel URL`
- `Discord Accounting Channel URL`

Each value must be a valid Discord webhook URL.

## Notifications

### Sales

When a sale order is confirmed, a Discord message is sent with information about the order.

### Stock

A scheduled cron job checks orderpoints and sends a message when:

- `qty_on_hand` is lower than `product_min_qty`
- `product_low_stock_already_sent_discord` is `False`

Example message:

> "Low stock of this product: Office Chair Black. Actual stock: 10.0. Minimum quantity we must have: 20.0."

### Accounting

A scheduled cron job checks invoices and sends a message when:

- the invoice is posted
- the due date is in the past
- `invoice_already_sent_discord` is `False`

Example message:

> "Expired invoice: INV/2026/00005 due on 2026-03-31."

## Cron jobs

The module defines these cron actions:

- `ir_cron_account_move_expired_invoices` → `account.move.action_cron_expired_invoices()`
- `ir_cron_stock_warehouse_orderpoint_low_stock` → `stock.warehouse.orderpoint.action_cron_low_stock()`

## Email fallback

If the configured webhook URL is missing or empty, the module sends an email using these templates:

- `discord_connector.email_template_link_not_configured_invoice`
- `discord_connector.email_template_link_not_configured_stock`
