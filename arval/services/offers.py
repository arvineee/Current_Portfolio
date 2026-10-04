"""Limited-time offers, managed from /admin/offer.

Stored in the settings table of projects.db (see database.py).
Times are entered and shown in Kenya time (EAT, UTC+3, no daylight saving).
An offer switches itself off the moment its end time passes — no cron job needed.
"""
import json
from datetime import datetime, timedelta, timezone

from arval import database

EAT = timezone(timedelta(hours=3))
SETTING_KEY = 'offer'
FORM_FORMAT = '%Y-%m-%dT%H:%M'   # value format of <input type="datetime-local">

DEFAULT = {
    'active': False,
    'title': 'Special Offer',
    'message': '',
    'discount_percent': 0,
    'overrides': {},       # {"0": 8000} -> fixed sale price for plan index 0
    'ends_at': '',         # 'YYYY-MM-DDTHH:MM' in EAT
}


def now():
    return datetime.now(EAT)


def parse_end(value):
    """'2026-10-20T23:59' (EAT) -> aware datetime, or None if invalid."""
    try:
        return datetime.strptime(value, FORM_FORMAT).replace(tzinfo=EAT)
    except (ValueError, TypeError):
        return None


def load():
    data = dict(DEFAULT)
    try:
        raw = database.get_setting(SETTING_KEY)
        if raw:
            data.update(json.loads(raw))
    except Exception:
        pass
    return data


def save(data):
    clean = dict(DEFAULT)
    clean.update(data)
    database.set_setting(SETTING_KEY, json.dumps(clean))


def get_active_offer():
    """Return the offer dict (with ends_at_iso / ends_at_label) if it is live now, else None."""
    data = load()
    if not data.get('active'):
        return None
    end = parse_end(data.get('ends_at'))
    if not end or end <= now():
        return None
    data['ends_at_iso'] = end.isoformat()                 # e.g. 2026-10-20T23:59:00+03:00
    data['ends_at_date'] = end.date().isoformat()
    data['ends_at_label'] = end.strftime('%d %b %Y, %I:%M %p') + ' EAT'
    return data


def _round10(x):
    return int(round(x / 10.0) * 10)


def apply_to_plans(plans, offer):
    """Copy of plans with sale_price / sale_price_value / percent_off added where an offer applies."""
    out = []
    pct = int(offer.get('discount_percent') or 0) if offer else 0
    overrides = (offer or {}).get('overrides') or {}
    for i, plan in enumerate(plans):
        p = dict(plan)
        base = p.get('price_value')
        if offer and base:
            sale = None
            if str(i) in overrides and overrides[str(i)]:
                sale = int(overrides[str(i)])
            elif pct > 0:
                sale = _round10(base * (100 - pct) / 100)
            if sale and 0 < sale < base:
                p['sale_price_value'] = sale
                p['sale_price'] = f'KES {sale:,}'
                p['percent_off'] = int(round((1 - sale / base) * 100))
        out.append(p)
    return out



def featured_plan_index(plans):
    """Index of the plan the offer banner's "Book Now" button should open.

    Prefers the highlighted plan if it is on sale, otherwise the first plan on sale.
    """
    on_sale = [i for i, p in enumerate(plans) if p.get('sale_price_value')]
    if not on_sale:
        return None
    return next((i for i in on_sale if plans[i].get('highlighted')), on_sale[0])
