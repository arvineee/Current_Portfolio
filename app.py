from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# ── Mail config (update with your real credentials) ──────────────────────────
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'kiruifelix03@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your_app_password')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME', 'your@gmail.com')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

mail = Mail(app)

OWNER_EMAIL = os.environ.get('MAIL_USERNAME', 'your@gmail.com')
WHATSAPP_NUMBER = '+254700000000'   # ← UPDATE WITH YOUR REAL NUMBER
PHONE_NUMBER = '+254700000000'      # ← UPDATE WITH YOUR REAL NUMBER

# ── Projects data (edit freely) ───────────────────────────────────────────────
PROJECTS = [
    {
        'title': 'CVForge AI',
        'description': 'A full SaaS CV builder powered by Gemini AI — users upload a CV, the AI parses and restructures it, and they download a polished PDF. Includes M-Pesa/Lipana STK Push payments, user accounts, and an admin dashboard.',
        'tags': ['Flask', 'Gemini AI', 'M-Pesa', 'PostgreSQL', 'PDF Generation'],
        'url': '#',
        'featured': True,
    },
    {
        'title': 'Arval Blog News',
        'description': 'A Kenya-focused news platform built for reach — Google News approved, Schema.org structured data, AI-citation optimised, automated social posting to X, and a full admin panel for publishing.',
        'tags': ['Flask', 'MySQL', 'Technical SEO', 'PythonAnywhere', 'Schema.org'],
        'url': 'https://arvalblognews.online',
        'featured': True,
    },
    {
        'title': 'SEO & Schema Implementation',
        'description': 'Took a Flask news site from invisible to Google News approved. Implemented NewsArticle schema, llms.txt for AI crawlers, OpenGraph tags, RSS feed, and sitemap rebuild — resulting in real organic traffic.',
        'tags': ['Technical SEO', 'Schema.org', 'Google News', 'Flask'],
        'url': '#',
        'featured': False,
    },
]

# ── Pricing plans ─────────────────────────────────────────────────────────────
PLANS = [
    {
        'name': 'Starter',
        'price': '$249',
        'period': 'one-time',
        'description': 'You need a real web presence — fast. No builders, no templates you can\'t control.',
        'features': [
            'Up to 5-page custom website',
            'Mobile-first responsive design',
            'Contact form with email delivery',
            'Basic on-page SEO setup',
            'Deployed and live on your domain',
            '30 days post-launch support',
        ],
        'cta': 'Get Started',
        'highlighted': False,
    },
    {
        'name': 'Professional',
        'price': '$499',
        'period': 'one-time',
        'description': 'A proper web application — user accounts, database, payments, admin panel. The whole thing.',
        'features': [
            'Custom Flask web application',
            'Database design & full backend',
            'User authentication system',
            'Payment gateway (M-Pesa or Stripe)',
            'Admin dashboard to manage content',
            'Full SEO + Schema.org setup',
            '90 days post-launch support',
        ],
        'cta': 'Most Popular',
        'highlighted': True,
    },
    {
        'name': 'Enterprise',
        'price': 'Custom',
        'period': 'quote',
        'description': 'Complex platforms, SaaS products, AI integrations, or ongoing monthly retainers.',
        'features': [
            'Everything in Professional',
            'AI/ML feature integrations',
            'Multi-user / SaaS architecture',
            'DevOps, server setup & monitoring',
            'Priority turnaround',
            'Ongoing retainer available',
        ],
        'cta': "Let's Talk",
        'highlighted': False,
    },
]


@app.route('/')
def index():
    return render_template('index.html',
                           projects=PROJECTS,
                           plans=PLANS,
                           whatsapp=WHATSAPP_NUMBER,
                           phone=PHONE_NUMBER)


@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    subject = data.get('subject', 'Portfolio Inquiry').strip()
    message = data.get('message', '').strip()

    if not all([name, email, message]):
        return jsonify({'success': False, 'error': 'Please fill in all required fields.'}), 400

    try:
        # Notify owner
        owner_msg = Message(
            subject=f'[Portfolio] {subject} — from {name}',
            recipients=[OWNER_EMAIL],
            body=f"""New message from your portfolio:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
"""
        )
        mail.send(owner_msg)

        # Auto-reply to client
        reply_msg = Message(
            subject='Thanks for reaching out — Arvine Felix',
            recipients=[email],
            body=f"""Hi {name},

Thanks for getting in touch! I've received your message and will get back to you within 24 hours.

Here's a summary of what you sent:

Subject: {subject}
Message: {message}

In the meantime, feel free to connect with me:
- WhatsApp: {WHATSAPP_NUMBER}
- X (Twitter): https://x.com/Arvinefelix
- LinkedIn: https://linkedin.com/in/arvinefelix

Best regards,
Arvine Felix
Web Developer & SEO Specialist
"""
        )
        mail.send(reply_msg)

        return jsonify({'success': True, 'message': "Message sent! I'll reply within 24 hours."})

    except Exception as e:
        return jsonify({'success': False, 'error': 'Failed to send message. Please try WhatsApp instead.'}), 500


if __name__ == '__main__':
    app.run(debug=True)
