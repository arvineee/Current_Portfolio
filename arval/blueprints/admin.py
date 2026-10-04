"""Admin area (/admin): login, projects, limited-time offer, analytics, orders."""
import hmac
from functools import wraps

from flask import (Blueprint, flash, redirect, render_template, request, session, url_for)

import content
from config import Config
from arval.repos import orders, projects, visitors
from arval.services import offers

bp = Blueprint('admin', __name__, url_prefix='/admin')


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return view(*args, **kwargs)
    return wrapper


def _to_int(value, default=0):
    try:
        return int(str(value).replace(',', '').strip())
    except (ValueError, TypeError):
        return default


def _split_tags(raw):
    return [t.strip() for t in (raw or '').split(',') if t.strip()]


# ── login / logout ────────────────────────────────────────────────────────────
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.dashboard'))
    error = None
    if request.method == 'POST':
        expected = Config.ADMIN_PASSWORD
        given = request.form.get('password', '')
        if not expected:
            error = 'Admin login is disabled: set the ADMIN_PASSWORD environment variable.'
        elif hmac.compare_digest(given.encode(), expected.encode()):
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            error = 'Incorrect password.'
    return render_template('admin/admin_login.html', error=error)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.login'))


# ── projects ──────────────────────────────────────────────────────────────────
@bp.route('/')
@login_required
def dashboard():
    return render_template('admin/admin.html', projects=projects.all_projects())


@bp.route('/projects/add', methods=['POST'])
@login_required
def add_project():
    f = request.form
    title, description = f.get('title', '').strip(), f.get('description', '').strip()
    if title and description:
        projects.create(title, description, _split_tags(f.get('tags')), f.get('url', '#').strip(),
                        f.get('github', '').strip(), f.get('featured') == 'on',
                        _to_int(f.get('sort_order')))
        flash('Project added.', 'success')
    else:
        flash('Title and description are required.', 'error')
    return redirect(url_for('admin.dashboard'))


@bp.route('/projects/<int:pid>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(pid):
    project = projects.get(pid)
    if not project:
        flash('Project not found.', 'error')
        return redirect(url_for('admin.dashboard'))
    if request.method == 'POST':
        f = request.form
        projects.update(pid, f.get('title', '').strip(), f.get('description', '').strip(),
                        _split_tags(f.get('tags')), f.get('url', '#').strip(),
                        f.get('github', '').strip(), f.get('featured') == 'on',
                        _to_int(f.get('sort_order')))
        flash('Project updated.', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/admin_edit.html', project=project)


@bp.route('/projects/<int:pid>/delete', methods=['POST'])
@login_required
def delete_project(pid):
    projects.delete(pid)
    flash('Project deleted.', 'success')
    return redirect(url_for('admin.dashboard'))


# ── offers ────────────────────────────────────────────────────────────────────
def _validate_offer(form, priced):
    """Return (offer data, error message or None) from the submitted offer form."""
    title = form.get('title', '').strip()
    pct = _to_int(form.get('discount_percent'))
    ends_at = form.get('ends_at', '').strip()
    active = form.get('active') == 'on'
    overrides = {}
    for i, _plan in priced:
        val = _to_int(form.get(f'sale_{i}'))
        if val:
            overrides[str(i)] = val

    error = None
    if not title:
        error = 'Give the offer a title.'
    elif not 0 <= pct <= 90:
        error = 'Discount % must be between 0 and 90.'
    elif not pct and not overrides:
        error = 'Set a discount % or a sale price for at least one plan.'
    elif any(v >= content.PLANS[int(i)]['price_value'] for i, v in overrides.items()):
        error = 'A sale price must be lower than the normal price.'
    else:
        end = offers.parse_end(ends_at)
        if not end:
            error = 'Pick an end date and time.'
        elif active and end <= offers.now():
            error = 'The end time must be in the future.'

    data = {'active': active, 'title': title, 'message': form.get('message', '').strip(),
            'discount_percent': pct, 'overrides': overrides, 'ends_at': ends_at}
    return data, error


@bp.route('/offer', methods=['GET', 'POST'])
@login_required
def offer():
    priced = [(i, p) for i, p in enumerate(content.PLANS) if p.get('price_value')]

    if request.method == 'POST':
        data, error = _validate_offer(request.form, priced)
        if error:
            flash(error, 'error')
            return render_template('admin/admin_offer.html', offer=data, priced=priced,
                                   live=None, preview=None, now_eat=offers.now())
        offers.save(data)
        flash('Offer saved — it is live on the site now.' if data['active']
              else 'Offer saved (switched off).', 'success')
        return redirect(url_for('admin.offer'))

    live = offers.get_active_offer()
    preview = offers.apply_to_plans(content.PLANS, live) if live else None
    return render_template('admin/admin_offer.html', offer=offers.load(), priced=priced,
                           live=live, preview=preview, now_eat=offers.now())


@bp.route('/offer/stop', methods=['POST'])
@login_required
def offer_stop():
    data = offers.load()
    data['active'] = False
    offers.save(data)
    flash('Offer ended — normal prices are showing.', 'success')
    return redirect(url_for('admin.offer'))


# ── analytics & orders ────────────────────────────────────────────────────────
@bp.route('/analytics')
@login_required
def analytics():
    days = min(max(request.args.get('days', 30, type=int), 1), 365)
    return render_template('admin/admin_analytics.html', data=visitors.analytics(days), days=days)


@bp.route('/orders')
@login_required
def orders_page():
    return render_template('admin/admin_orders.html', orders=orders.recent(), totals=orders.totals())
