from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_mail import Mail, Message
from functools import wraps
import config
import db as database

app = Flask(__name__)

# ── CONFIG ────────────────────────────────────────────────────────────────────
app.config['MAIL_SERVER']       = config.MAIL_SERVER
app.config['MAIL_PORT']         = config.MAIL_PORT
app.config['MAIL_USE_TLS']      = config.MAIL_USE_TLS
app.config['MAIL_USERNAME']     = config.MAIL_USERNAME
app.config['MAIL_PASSWORD']     = config.MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = config.MAIL_DEFAULT_SENDER
app.config['SECRET_KEY']        = config.SECRET_KEY

mail = Mail(app)

# Initialise DB + seed from config.PROJECTS on first run
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


# ── ADMIN AUTH DECORATOR ──────────────────────────────────────────────────────
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


# ── ADMIN: LOGIN / LOGOUT ──────────────────────────────────────────────────────
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))

    error = None
    if request.method == 'POST':
        pwd = request.form.get('password', '')
        if pwd == config.ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        error = 'Incorrect password.'

    return render_template('admin_login.html', error=error)


@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))


# ── ADMIN: DASHBOARD (list projects) ─────────────────────────────────────────
@app.route('/admin')
@login_required
def admin_dashboard():
    projects = database.get_all_projects()
    return render_template('admin.html', projects=projects)


# ── ADMIN: ADD PROJECT ────────────────────────────────────────────────────────
@app.route('/admin/projects/add', methods=['POST'])
@login_required
def admin_add_project():
    title       = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    tags_raw    = request.form.get('tags', '')
    url         = request.form.get('url', '#').strip()
    github      = request.form.get('github', '').strip()
    featured    = request.form.get('featured') == 'on'
    sort_order  = int(request.form.get('sort_order', 0) or 0)

    tags = [t.strip() for t in tags_raw.split(',') if t.strip()]

    if title and description:
        database.create_project(title, description, tags, url, github, featured, sort_order)
        flash('Project added successfully.', 'success')
    else:
        flash('Title and description are required.', 'error')

    return redirect(url_for('admin_dashboard'))


# ── ADMIN: EDIT PROJECT (GET form + POST save) ────────────────────────────────
@app.route('/admin/projects/<int:pid>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_project(pid):
    project = database.get_project(pid)
    if not project:
        flash('Project not found.', 'error')
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        title       = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        tags_raw    = request.form.get('tags', '')
        url         = request.form.get('url', '#').strip()
        github      = request.form.get('github', '').strip()
        featured    = request.form.get('featured') == 'on'
        sort_order  = int(request.form.get('sort_order', 0) or 0)
        tags = [t.strip() for t in tags_raw.split(',') if t.strip()]

        database.update_project(pid, title, description, tags, url, github, featured, sort_order)
        flash('Project updated.', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_edit.html', project=project)


# ── ADMIN: DELETE PROJECT ─────────────────────────────────────────────────────
@app.route('/admin/projects/<int:pid>/delete', methods=['POST'])
@login_required
def admin_delete_project(pid):
    database.delete_project(pid)
    flash('Project deleted.', 'success')
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    app.run(debug=True)

