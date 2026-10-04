# Arval Web Solutions — portfolio & services site

Flask app: portfolio, pricing, limited-time offers, contact form, admin panel, analytics,
and **IntaSend checkout** (M-Pesa STK Push + card) behind the "Book Now" buttons.

## Layout

```
app.py                  entry point (exposes `app` — your PythonAnywhere WSGI file keeps working)
config.py               settings + secrets, all from environment variables
content.py              site copy: PROJECTS, PLANS, SERVICES, FAQS  (edit prices/text here)
arval/
  __init__.py           create_app() — wires everything together
  database.py           SQLite connection helper, schema, settings table
  security.py           security headers, noindex for private paths, admin cross-site guard
  extensions.py         Flask-Mail instance
  repos/                database access only: projects, visitors, orders
  services/             business logic: offers, catalog (live prices), seo, tracking, mailer, payments (IntaSend)
  blueprints/           routes only: public, seo_pages, payments, admin
templates/
  base.html             shared <head>, fonts, WhatsApp button
  index.html            home page = base + templates/home/_*.html section partials
  contact.html
  payments/             checkout.html, status.html
  admin/                admin pages (+ new admin_orders.html)
static/js/              offer.js, contact.js, payment-status.js  (css/style.css, js/main.js, AF.jpg: unchanged, keep yours)
```

Rule of thumb: routes call services, services call repos, repos talk to SQLite.

## Deploying over your current version (PythonAnywhere)

1. Upload this folder over the old files. **Keep** your existing `static/css/style.css`, `static/js/main.js`,
   `static/AF.jpg` and `projects.db` (the new code reads the same database and adds an `orders` table automatically).
   Delete the old root-level `db.py`, `offers.py`, `seo.py` and flat `admin*.html`/`index.html` copies.
2. `pip install --user -r requirements.txt`
3. Set environment variables (see `.env.example`) in the WSGI file, e.g. `os.environ['SECRET_KEY'] = '...'`
   **before** `from app import app as application`.
   `ADMIN_PASSWORD` is required — the old code referenced it but `config.py` never defined it, so admin login would have crashed.
4. Reload the web app.

## IntaSend setup

1. Create an account at intasend.com, then Developers → API keys. Start with the **sandbox** keys.
2. Set `INTASEND_SECRET_KEY`, `INTASEND_PUBLISHABLE_KEY`, `INTASEND_TEST_MODE=true`.
3. Dashboard → Webhooks → add `https://<your-site>/webhooks/intasend` and enter a challenge string;
   put the same string in `INTASEND_WEBHOOK_CHALLENGE`.
4. Make a test booking on the site. Check **Admin → Orders**: it should go pending → paid.
5. Going live: swap in the live keys and set `INTASEND_TEST_MODE=false`.

How it works: the customer picks a plan → `/checkout/<plan>` (name, email, M-Pesa number) → we create an order and
get a hosted IntaSend checkout URL → customer pays by M-Pesa or card → IntaSend calls the webhook → we verify the
challenge, re-fetch the invoice from IntaSend, check the amount, mark the order paid and email you both.
The price is always computed on the server (including live offers), never taken from the browser.

`PAYMENT_DEPOSIT_PERCENT` (default 100) lets you collect a deposit instead of the full price —
useful because the Web App plan is priced "from KES 15,000".

If the IntaSend keys aren't set, "Book Now" buttons quietly fall back to the contact form / WhatsApp.

## Admin

`/admin` — Projects · Analytics · **Orders** · Offer (`/admin/offer`). Offer banner now has a **Book Now** button
that opens checkout for the discounted plan (highlighted plan first).
