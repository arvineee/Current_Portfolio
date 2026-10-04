"""Checkout pages, the return/status pages and the IntaSend webhook."""
import hmac
import re

from flask import (Blueprint, abort, current_app, jsonify, redirect, render_template,
                   request, url_for)

from config import Config
from arval.repos import orders
from arval.services import catalog, payments

bp = Blueprint('payments', __name__)

EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


def payments_enabled():
    return payments.is_configured()


def _checkout_context(plan_index, plan, form=None, error=None):
    offer, _, _ = catalog.offer_context()
    return {
        'plan': plan, 'plan_index': plan_index, 'offer': offer,
        'price': catalog.current_price(plan),
        'amount': catalog.amount_due(plan),
        'deposit_percent': Config.PAYMENT_DEPOSIT_PERCENT,
        'currency': Config.PAYMENT_CURRENCY,
        'enabled': payments.is_configured(),
        'form': form or {}, 'error': error,
    }


@bp.route('/checkout/<int:plan_index>', methods=['GET', 'POST'])
def checkout(plan_index):
    plan = catalog.find_plan(plan_index)
    if not catalog.is_payable(plan):                  # custom-quote plans go through the contact form
        return redirect(url_for('public.contact'))

    if request.method == 'GET':
        return render_template('payments/checkout.html', **_checkout_context(plan_index, plan))

    form = {k: (request.form.get(k) or '').strip() for k in ('name', 'email', 'phone')}
    phone = payments.normalize_phone(form['phone'])
    error = None
    if len(form['name']) < 2:
        error = 'Please enter your name.'
    elif not EMAIL_RE.match(form['email']):
        error = 'Please enter a valid email address.'
    elif not phone:
        error = 'Enter a valid Kenyan mobile number, e.g. 0712 345 678.'
    elif not payments.is_configured():
        error = 'Online payment is not available right now. Please contact me on WhatsApp.'
    if error:
        return render_template('payments/checkout.html',
                               **_checkout_context(plan_index, plan, form, error)), 400

    # The amount always comes from the server-side price list, never from the browser.
    offer, _, _ = catalog.offer_context()
    ref = orders.create(plan_index, plan['name'], plan['price_value'], catalog.amount_due(plan),
                        offer['title'] if offer and plan.get('sale_price_value') else '',
                        form['name'], form['email'], phone)
    return_url = f"{Config.SITE_URL}{url_for('payments.return_page', ref=ref)}"
    try:
        checkout_url = payments.create_checkout(orders.get(ref), return_url)
    except payments.PaymentError as exc:
        orders.mark_failed_to_start(ref, str(exc))
        return render_template(
            'payments/checkout.html',
            **_checkout_context(plan_index, plan, form,
                                'We could not start the payment. Please try again or use WhatsApp.')), 502
    return redirect(checkout_url)


@bp.route('/pay/return')
def return_page():
    order = orders.get(request.args.get('ref', ''))
    if not order:
        abort(404)
    return render_template('payments/status.html', order=order)


@bp.route('/pay/status/<ref>')
def status(ref):
    order = orders.get(ref)
    if not order:
        abort(404)
    return jsonify({'status': order['status'], 'plan': order['plan_name'], 'amount': order['amount']})


@bp.route('/webhooks/intasend', methods=['POST'])
def intasend_webhook():
    expected = Config.INTASEND_WEBHOOK_CHALLENGE
    if not expected:
        return jsonify({'ok': False, 'error': 'webhook not configured'}), 503
    payload = request.get_json(silent=True) or request.form.to_dict() or {}
    if not hmac.compare_digest(str(payload.get('challenge', '')), expected):
        return jsonify({'ok': False, 'error': 'bad challenge'}), 403
    try:
        result = payments.handle_webhook(payload)
    except payments.PaymentError:
        return jsonify({'ok': False}), 502            # IntaSend will retry
    current_app.logger.info('IntaSend webhook for %s: %s', payload.get('api_ref'), result)
    return jsonify({'ok': True})
