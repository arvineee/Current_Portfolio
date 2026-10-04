"""IntaSend payments (M-Pesa STK Push + card) through IntaSend's hosted checkout.

Flow
  1. The customer submits the checkout form -> we create an order and call IntaSend
     `collect.checkout(...)`, which returns a hosted payment URL (M-Pesa and card).
  2. The customer pays on IntaSend's page and is sent back to /pay/return?ref=<order ref>.
  3. IntaSend calls our webhook. We check the shared challenge, then ask IntaSend for the
     invoice itself (we never trust the webhook body alone) and settle the order.
"""
import re
from decimal import Decimal, InvalidOperation

from flask import current_app

from config import Config as cfg
from arval.repos import orders
from arval.services import mailer


class PaymentError(Exception):
    """Raised when IntaSend can't be reached or refuses a request. Message is safe to log."""


def is_configured():
    return bool(cfg.INTASEND_SECRET_KEY and cfg.INTASEND_PUBLISHABLE_KEY)


def normalize_phone(raw):
    """'0712 345 678' / '+254712345678' / '712345678' -> '254712345678', or None if invalid."""
    digits = re.sub(r'\D', '', raw or '')
    if len(digits) == 12 and digits.startswith('254'):
        pass
    elif len(digits) == 10 and digits.startswith('0'):
        digits = '254' + digits[1:]
    elif len(digits) == 9 and digits[0] in '71':
        digits = '254' + digits
    else:
        return None
    return digits if digits[3] in '71' else None       # Safaricom/Airtel ranges: 07xx and 01xx


def _service():
    try:
        from intasend import APIService
    except ImportError as exc:
        raise PaymentError('intasend-python is not installed (pip install intasend-python)') from exc
    return APIService(token=cfg.INTASEND_SECRET_KEY,
                      publishable_key=cfg.INTASEND_PUBLISHABLE_KEY,
                      test=cfg.INTASEND_TEST_MODE)


def create_checkout(order, redirect_url):
    """Ask IntaSend for a hosted checkout URL for this order and return it."""
    first, _, last = order['customer_name'].partition(' ')
    try:
        resp = _service().collect.checkout(
            phone_number=order['phone'],
            email=order['email'],
            amount=order['amount'],
            currency=cfg.PAYMENT_CURRENCY,
            comment=f"{order['plan_name']} ({order['ref']})",
            redirect_url=redirect_url,
            api_ref=order['ref'],
            first_name=first,
            last_name=last,
        )
    except PaymentError:
        raise
    except Exception as exc:
        current_app.logger.exception('IntaSend checkout failed for %s', order['ref'])
        raise PaymentError(f'IntaSend checkout failed: {exc}') from exc

    url = (resp or {}).get('url')
    if not url:
        raise PaymentError(f'IntaSend returned no checkout URL: {resp}')
    orders.set_checkout(order['ref'], str((resp or {}).get('id', '')))
    return url


def fetch_invoice(invoice_id):
    """The authoritative invoice record from IntaSend (state, value, api_ref, ...)."""
    try:
        resp = _service().collect.status(invoice_id=invoice_id)
    except PaymentError:
        raise
    except Exception as exc:
        current_app.logger.exception('IntaSend status check failed for %s', invoice_id)
        raise PaymentError(f'IntaSend status check failed: {exc}') from exc
    return (resp or {}).get('invoice') or resp or {}


def _to_decimal(value):
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError):
        return Decimal(0)


def handle_webhook(payload):
    """Verify a (challenge-checked) webhook against IntaSend and settle the matching order.

    Returns a short string describing what happened. Raises PaymentError if IntaSend could
    not be reached — the caller should answer 5xx so IntaSend retries the webhook.
    """
    ref = str(payload.get('api_ref') or '')
    invoice_id = str(payload.get('invoice_id') or '')
    order = orders.get(ref) if ref else None
    if not order or not invoice_id:
        return 'ignored: unknown order'

    invoice = fetch_invoice(invoice_id)
    if invoice.get('api_ref') and str(invoice['api_ref']) != ref:
        return 'ignored: invoice belongs to a different order'

    state = str(invoice.get('state') or '').upper()
    if state == 'COMPLETE':
        if _to_decimal(invoice.get('value')) < Decimal(order['amount']):
            orders.settle(ref, 'review', invoice_id, state, 'Paid amount is lower than the order amount')
            return 'flagged: amount mismatch'
        if orders.settle(ref, 'paid', invoice_id, state):
            try:
                mailer.send_payment_emails(orders.get(ref))
            except Exception:
                current_app.logger.exception('Payment emails failed for %s', ref)
        return 'paid'

    if state == 'FAILED':
        reason = invoice.get('failed_reason') or invoice.get('failed_code') or 'Payment failed'
        orders.settle(ref, 'failed', invoice_id, state, str(reason))
        return 'failed'

    orders.settle(ref, 'pending', invoice_id, state)       # PENDING / PROCESSING: keep waiting
    return f'pending ({state or "unknown"})'
