from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_mail import Mail, Message
from functools import wraps
import config
import db as database
import seo
import offers

app = Flask(__name__)

# ── CONFIG ────────────────────────────────────────────────────────────────────
app.config['MAIL_SERVER']         = config.MAIL_SERVER
app.config['MAIL_PORT']           = config.MAIL_PORT
app.config['MAIL_USE_TLS']        = config.MAIL_USE_TLS
app.config['MAIL_USERNAME']       = config.MAIL_USERNAME
app.config['MAIL_PASSWORD']       = config.MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = config.MAIL_DEFAULT_SENDER
app.config['SECRET_KEY']          = config.SECRET_KEY

app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'   # basic CSRF protection for admin forms
app.config['SESSION_COOKIE_HTTPONLY'] = True

mail = Mail(app)

with app.app_context():
    database.init_db()


# ── SECURITY HEADERS ──────────────────────────────────────────────────────────
@app.after_request
def set_security_headers(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self'; "
        "frame-ancestors 'none';"
    )
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['X-Frame-Options']            = 'DENY'
    response.headers['X-Content-Type-Options']     = 'nosniff'
    response.headers['Referrer-Policy']            = 'strict-origin-when-cross-origin'
    # Keep the admin area out of search results even if a link leaks.
    if request.path.startswith('/admin'):
        response.headers['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
    # Let search engines cache static assets / feeds sensibly.
    if request.path in ('/sitemap.xml', '/robots.txt'):
        response.headers['Cache-Control'] = 'public, max-age=3600'
    return response


# ── VISITOR TRACKING HELPERS ──────────────────────────────────────────────────
def _parse_ua(ua):
    """Return (device, browser, os) strings from User-Agent."""
    ua = ua or ''
    ul = ua.lower()

    # Device
    if any(x in ul for x in ('mobile', 'android', 'iphone')):
        device = 'mobile'
    elif 'tablet' in ul or 'ipad' in ul:
        device = 'tablet'
    else:
        device = 'desktop'

    # Browser
    if 'edg' in ul:
        browser = 'Edge'
    elif 'opr' in ul or 'opera' in ul:
        browser = 'Opera'
    elif 'chrome' in ul:
        browser = 'Chrome'
    elif 'firefox' in ul:
        browser = 'Firefox'
    elif 'safari' in ul:
        browser = 'Safari'
    else:
        browser = 'Other'

    # OS
    if 'windows' in ul:
        os_name = 'Windows'
    elif 'android' in ul:
        os_name = 'Android'
    elif 'iphone' in ul or 'ipad' in ul:
        os_name = 'iOS'
    elif 'mac' in ul:
        os_name = 'macOS'
    elif 'linux' in ul:
        os_name = 'Linux'
    else:
        os_name = 'Other'

    return device, browser, os_name


def _get_location(ip):
    """Return (country, city) via ip-api.com free tier (no key needed)."""
    try:
        import urllib.request, json as _json
        with urllib.request.urlopen(
            f'http://ip-api.com/json/{ip}?fields=country,city,status',
            timeout=2
        ) as resp:
            data = _json.loads(resp.read())
            if data.get('status') == 'success':
                return data.get('country', 'Unknown'), data.get('city', '')
    except Exception:
        pass
    return 'Unknown', ''


def _real_ip():
    """Get real IP behind PythonAnywhere's proxy."""
    return (
        request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
        or request.headers.get('X-Real-IP', '')
        or request.remote_addr
        or ''
    )


def track_visit():
    """Log a page visit — skip bots and admin routes."""
    path = request.path
    # Skip admin, static, and bot-like paths
    if path.startswith('/admin') or path.startswith('/static'):
        return
    ua = request.headers.get('User-Agent', '')
    if any(b in ua.lower() for b in ('bot', 'crawler', 'spider', 'curl', 'wget', 'python-requests')):
        return

    ip       = _real_ip()
    referrer = request.referrer or ''
    # Strip own domain from referrer
    if referrer and request.host in referrer:
        referrer = ''

    country, city    = _get_location(ip)
    device, browser, os_name = _parse_ua(ua)

    database.log_visitor(path, ip, country, city, device, browser, os_name, referrer)


# ── ADMIN AUTH ────────────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated


def _offer_context():
    """Live offer (or None) plus the plans with sale prices applied."""
    offer = offers.get_active_offer()
    plans = offers.apply_to_plans(config.PLANS, offer) if offer else config.PLANS
    return offer, plans


# ── PUBLIC ROUTES ─────────────────────────────────────────────────────────────
@app.route('/')
def index():
    track_visit()
    projects = database.get_all_projects()
    offer, plans = _offer_context()
    return render_template('index.html',
                           projects=projects,
                           plans=plans,
                           offer=offer,
                           services=config.SERVICES,
                           faqs=config.FAQS,
                           schema=seo.build_home_schema(plans, offer),
                           site_url=config.SITE_URL,
                           whatsapp=config.WHATSAPP_NUMBER,
                           phone=config.PHONE_NUMBER,
                           owner_email=config.OWNER_EMAIL)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        track_visit()
        return render_template('contact.html',
                               schema=seo.build_contact_schema(),
                               site_url=config.SITE_URL,
                               whatsapp=config.WHATSAPP_NUMBER,
                               phone=config.PHONE_NUMBER,
                               owner_email=config.OWNER_EMAIL)

    data    = request.get_json() or {}
    name    = data.get('name', '').strip()
    email   = data.get('email', '').strip()
    subject = data.get('subject', 'Portfolio Inquiry').strip()
    message = data.get('message', '').strip()

    if not all([name, email, message]):
        return jsonify({'success': False, 'error': 'Please fill in all required fields.'}), 400

    try:
        mail.send(Message(
            subject=f'[Portfolio Inbound] {subject} — from {name}',
            recipients=[config.OWNER_EMAIL],
            body=f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\n{message}"
        ))
        mail.send(Message(
            subject='Project Request Received — Arvine Felix',
            recipients=[email],
            body=f"""Hi {name},

Thanks for reaching out! I've received your message and will get back to you within 24 hours with a clear plan and price.

Subject: {subject}
Message: {message}

If it's urgent, feel free to message me directly:
- WhatsApp: https://wa.me/{config.WHATSAPP_NUMBER.replace('+', '')}
- X: https://x.com/Arvinefelix
- LinkedIn: https://linkedin.com/in/arvinefelix

Talk soon,
Arvine Felix
Web Developer · Nairobi, Kenya
"""
        ))
        return jsonify({'success': True, 'message': 'Message sent! I will respond within 24 hours.'})
    except Exception:
        return jsonify({'success': False, 'error': 'Email dispatch failed. Please use WhatsApp instead.'}), 500


@app.route('/google8caacc303a714c4c.html')
def verify():
    return render_template('google8caacc303a714c4c.html')


@app.route('/robots.txt')
def robots():
    # One group for everyone (search engines AND AI crawlers such as GPTBot, ClaudeBot,
    # PerplexityBot, Google-Extended): public pages are open, admin is closed.
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin",
        "",
        f"Sitemap: {config.SITE_URL}/sitemap.xml",
    ]
    return app.response_class("\n".join(lines) + "\n", mimetype='text/plain')


@app.route('/sitemap.xml')
def sitemap():
    base = config.SITE_URL
    lastmod = config.CONTENT_LAST_MODIFIED
    urls = [
        {'loc': f'{base}/', 'changefreq': 'weekly', 'priority': '1.0',
         'image': f'{base}/static/AF.jpg'},
        {'loc': f'{base}/contact', 'changefreq': 'monthly', 'priority': '0.8'},
    ]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for u in urls:
        img = (f"<image:image><image:loc>{u['image']}</image:loc></image:image>"
               if u.get('image') else '')
        xml.append(
            f"<url><loc>{u['loc']}</loc><lastmod>{lastmod}</lastmod>"
            f"<changefreq>{u['changefreq']}</changefreq><priority>{u['priority']}</priority>{img}</url>"
        )
    xml.append('</urlset>')
    return app.response_class("\n".join(xml), mimetype='application/xml')


@app.route('/llms.txt')
def llms_txt():
    """Plain-text briefing for AI assistants / answer engines (the page already links to it)."""
    offer, plans = _offer_context()
    return app.response_class(seo.build_llms_txt(plans, offer), mimetype='text/plain; charset=utf-8')


# ── ADMIN: LOGIN / LOGOUT ─────────────────────────────────────────────────────
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
    error = None
    if request.method == 'POST':
        if request.form.get('password', '') == config.ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        error = 'Incorrect password.'
    return render_template('admin_login.html', error=error)


@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))


# ── ADMIN: PROJECTS DASHBOARD ─────────────────────────────────────────────────
@app.route('/admin')
@login_required
def admin_dashboard():
    projects = database.get_all_projects()
    return render_template('admin.html', projects=projects)


@app.route('/admin/projects/add', methods=['POST'])
@login_required
def admin_add_project():
    title      = request.form.get('title', '').strip()
    description= request.form.get('description', '').strip()
    tags       = [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()]
    url        = request.form.get('url', '#').strip()
    github     = request.form.get('github', '').strip()
    featured   = request.form.get('featured') == 'on'
    sort_order = int(request.form.get('sort_order', 0) or 0)
    if title and description:
        database.create_project(title, description, tags, url, github, featured, sort_order)
        flash('Project added.', 'success')
    else:
        flash('Title and description are required.', 'error')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/projects/<int:pid>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_project(pid):
    project = database.get_project(pid)
    if not project:
        flash('Project not found.', 'error')
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        tags = [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()]
        database.update_project(
            pid,
            request.form.get('title', '').strip(),
            request.form.get('description', '').strip(),
            tags,
            request.form.get('url', '#').strip(),
            request.form.get('github', '').strip(),
            request.form.get('featured') == 'on',
            int(request.form.get('sort_order', 0) or 0)
        )
        flash('Project updated.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit.html', project=project)


@app.route('/admin/projects/<int:pid>/delete', methods=['POST'])
@login_required
def admin_delete_project(pid):
    database.delete_project(pid)
    flash('Project deleted.', 'success')
    return redirect(url_for('admin_dashboard'))


# ── ADMIN: OFFERS ─────────────────────────────────────────────────────────────
@app.route('/admin/offer', methods=['GET', 'POST'])
@login_required
def admin_offer():
    priced = [(i, p) for i, p in enumerate(config.PLANS) if p.get('price_value')]

    if request.method == 'POST':
        def to_int(v):
            try:
                return int(str(v).replace(',', '').strip())
            except (ValueError, TypeError):
                return 0

        title   = request.form.get('title', '').strip()
        message = request.form.get('message', '').strip()
        pct     = to_int(request.form.get('discount_percent'))
        ends_at = request.form.get('ends_at', '').strip()
        active  = request.form.get('active') == 'on'
        overrides = {}
        for i, p in priced:
            val = to_int(request.form.get(f'sale_{i}'))
            if val:
                overrides[str(i)] = val

        error = None
        if not title:
            error = 'Give the offer a title.'
        elif not 0 <= pct <= 90:
            error = 'Discount % must be between 0 and 90.'
        elif not pct and not overrides:
            error = 'Set a discount % or a sale price for at least one plan.'
        elif any(v >= config.PLANS[int(i)]['price_value'] for i, v in overrides.items()):
            error = 'A sale price must be lower than the normal price.'
        else:
            end = offers.parse_end(ends_at)
            if not end:
                error = 'Pick an end date and time.'
            elif active and end <= offers.now():
                error = 'The end time must be in the future.'

        data = {'active': active, 'title': title, 'message': message,
                'discount_percent': pct, 'overrides': overrides, 'ends_at': ends_at}
        if error:
            flash(error, 'error')
            return render_template('admin_offer.html', offer=data, priced=priced,
                                   live=None, preview=None, now_eat=offers.now())
        offers.save(data)
        flash('Offer saved — it is live on the site now.' if active else 'Offer saved (switched off).', 'success')
        return redirect(url_for('admin_offer'))

    data = offers.load()
    live = offers.get_active_offer()
    preview = offers.apply_to_plans(config.PLANS, live) if live else None
    return render_template('admin_offer.html', offer=data, priced=priced,
                           live=live, preview=preview, now_eat=offers.now())


@app.route('/admin/offer/stop', methods=['POST'])
@login_required
def admin_offer_stop():
    data = offers.load()
    data['active'] = False
    offers.save(data)
    flash('Offer ended — normal prices are showing.', 'success')
    return redirect(url_for('admin_offer'))


# ── ADMIN: ANALYTICS ──────────────────────────────────────────────────────────
@app.route('/admin/analytics')
@login_required
def admin_analytics():
    days = int(request.args.get('days', 30))
    data = database.get_analytics(days)
    return render_template('admin_analytics.html', data=data, days=days)


if __name__ == '__main__':
    app.run(debug=False)




