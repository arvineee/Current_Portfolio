"""What is for sale right now: plans with any live offer applied, and what a plan costs today."""
import content
from config import Config
from arval.services import offers


def offer_context():
    """(live offer or None, plans with sale prices applied, featured plan index or None)."""
    offer = offers.get_active_offer()
    plans = offers.apply_to_plans(content.PLANS, offer) if offer else content.PLANS
    featured = offers.featured_plan_index(plans) if offer else None
    return offer, plans, featured


def find_plan(index):
    """The plan at `index` with live offer prices applied, or None."""
    _, plans, _ = offer_context()
    return plans[index] if 0 <= index < len(plans) else None


def is_payable(plan):
    return bool(plan and plan.get('price_value'))


def current_price(plan):
    """Price the customer pays today for the whole plan (sale price if on offer)."""
    return int(plan.get('sale_price_value') or plan['price_value'])


def amount_due(plan):
    """Amount collected online: the whole price, or a deposit share if configured."""
    price = current_price(plan)
    pct = Config.PAYMENT_DEPOSIT_PERCENT
    return price if pct >= 100 else max(1, round(price * pct / 100))
