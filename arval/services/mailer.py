"""All outgoing email lives here so routes stay thin."""
from flask_mail import Message

from config import Config
from arval.extensions import mail


def _wa_link():
    return f"https://wa.me/{Config.WHATSAPP_NUMBER.replace('+', '')}"


def send_contact_message(name, email, subject, message):
    """Notify the owner and send the visitor an acknowledgement. Raises on SMTP failure."""
    mail.send(Message(
        subject=f'[Portfolio Inbound] {subject} — from {name}',
        recipients=[Config.OWNER_EMAIL],
        body=f'Name: {name}\nEmail: {email}\nSubject: {subject}\n\n{message}'))
    mail.send(Message(
        subject='Project Request Received — Arvine Felix',
        recipients=[email],
        body=f"""Hi {name},

Thanks for reaching out! I've received your message and will get back to you within 24 hours with a clear plan and price.

Subject: {subject}
Message: {message}

If it's urgent, feel free to message me directly:
- WhatsApp: {_wa_link()}
- X: https://x.com/Arvinefelix
- LinkedIn: https://linkedin.com/in/arvinefelix

Talk soon,
Arvine Felix
Web Developer · Nairobi, Kenya
"""))


def send_payment_emails(order):
    """Tell the owner about the sale and send the customer a receipt."""
    amount = f"{Config.PAYMENT_CURRENCY} {order['amount']:,}"
    mail.send(Message(
        subject=f"[Payment received] {order['plan_name']} — {amount}",
        recipients=[Config.OWNER_EMAIL],
        body=(f"Order {order['ref']} is paid.\n\nPlan: {order['plan_name']}\nAmount: {amount}\n"
              f"Customer: {order['customer_name']}\nEmail: {order['email']}\nPhone: {order['phone']}\n"
              f"IntaSend invoice: {order['invoice_id']}\n")))
    mail.send(Message(
        subject=f"Payment received — {order['plan_name']} ({order['ref']})",
        recipients=[order['email']],
        body=f"""Hi {order['customer_name']},

Thank you — your payment of {amount} for "{order['plan_name']}" has been received.
Reference: {order['ref']}

I'll contact you within 24 hours to kick off your project and agree on the details.
Questions in the meantime? WhatsApp me: {_wa_link()}

Arvine Felix
Arval Web Solutions · Nairobi, Kenya
"""))
