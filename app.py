from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_mail import Mail, Message
from functools import wraps
import config
import db as database

app = Flask(__name__)

# ── CONFIG ────────────────────────────────────────────────────────────────────
app.config['MAIL_SERVER']         = config.MAIL_SERVER
app.config['MAIL_PORT']           = config.MAIL_PORT
app.config['MAIL_USE_TLS']        = config.MAIL_USE_TLS
app.config['MAIL_USERNAME']       = config.MAIL_USERNAME
app.config['MAIL_PASSWORD']       = config.MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = config.MAIL_DEFAULT_SENDER
app.config['SECRET_KEY']          = config.SECRET_KEY

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


# ── PUBLIC ROUTES ─────────────────────────────────────────────────────────────
@app.route('/')
def index():
    track_visit()
    projects = database.get_all_projects()
    return render_template('index.html',
                           projects=projects,
                           plans=config.PLANS,
                           whatsapp=config.WHATSAPP_NUMBER,
                           phone=config.PHONE_NUMBER,
                           owner_email=config.OWNER_EMAIL)


@app.route('/contact', methods=['POST'])
def contact():
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

Thank you for reaching out! I have received your project details and will respond within 24 hours.

Subject: {subject}
Message: {message}

Direct channels:
- WhatsApp: https://wa.me/{config.WHATSAPP_NUMBER.replace('+', '')}
- X: https://x.com/Arvinefelix
- LinkedIn: https://linkedin.com/in/arvinefelix

Best regards,
Arvine Felix
Full-Stack Software Developer · Nairobi, Kenya
"""
        ))
        return jsonify({'success': True, 'message': 'Message sent! I will respond within 24 hours.'})
    except Exception:
        return jsonify({'success': False, 'error': 'Email dispatch failed. Please use WhatsApp instead.'}), 500


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


# ── ADMIN: ANALYTICS ──────────────────────────────────────────────────────────
@app.route('/admin/analytics')
@login_required
def admin_analytics():
    days = int(request.args.get('days', 30))
    data = database.get_analytics(days)
    return render_template('admin_analytics.html', data=data, days=days)


if __name__ == '__main__':
    app.run(debug=True)

