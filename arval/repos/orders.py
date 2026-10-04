"""Orders: one row per checkout attempt. Status: pending -> paid | failed."""
import secrets
from datetime import datetime, timezone

from arval.database import connect


def _now():
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')


def new_ref():
    return 'AV-' + secrets.token_hex(5).upper()      # e.g. AV-3F9A1C07BE


def create(plan_index, plan_name, list_price, amount, offer_title,
           customer_name, email, phone):
    ref = new_ref()
    with connect() as conn:
        conn.execute(
            'INSERT INTO orders (ref,plan_index,plan_name,list_price,amount,offer_title,'
            'customer_name,email,phone,created_at) VALUES (?,?,?,?,?,?,?,?,?,?)',
            (ref, plan_index, plan_name, list_price, amount, offer_title,
             customer_name, email, phone, _now()))
    return ref


def get(ref):
    with connect() as conn:
        row = conn.execute('SELECT * FROM orders WHERE ref=?', (ref,)).fetchone()
    return dict(row) if row else None


def set_checkout(ref, checkout_id):
    with connect() as conn:
        conn.execute('UPDATE orders SET checkout_id=? WHERE ref=?', (checkout_id, ref))


def mark_failed_to_start(ref, reason):
    with connect() as conn:
        conn.execute("UPDATE orders SET status='failed', failure_reason=? "
                     "WHERE ref=? AND status='pending'", (reason[:300], ref))


def settle(ref, status, invoice_id='', provider_state='', reason=''):
    """Apply a provider result. Returns True only when the order newly became 'paid'.

    A paid order is final: later FAILED/PENDING events never overwrite it.
    """
    with connect() as conn:
        if status == 'paid':
            cur = conn.execute(
                "UPDATE orders SET status='paid', invoice_id=?, provider_state=?, paid_at=?, "
                "failure_reason='' WHERE ref=? AND status!='paid'",
                (invoice_id, provider_state, _now(), ref))
            return cur.rowcount == 1
        conn.execute(
            "UPDATE orders SET status=?, invoice_id=?, provider_state=?, failure_reason=? "
            "WHERE ref=? AND status!='paid'",
            (status, invoice_id, provider_state, reason[:300], ref))
        return False


def recent(limit=100):
    with connect() as conn:
        rows = conn.execute('SELECT * FROM orders ORDER BY id DESC LIMIT ?', (limit,)).fetchall()
    return [dict(r) for r in rows]


def totals():
    with connect() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS n, "
            "SUM(status='paid') AS paid, SUM(status='pending') AS pending, SUM(status='failed') AS failed, "
            "COALESCE(SUM(CASE WHEN status='paid' THEN amount END), 0) AS revenue FROM orders").fetchone()
    return {k: (row[k] or 0) for k in row.keys()}
