from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# ── Mail config (fallback to environment variables or local credentials) ──
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'kiruifelix03@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your_app_password')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME', 'kiruifelix03@gmail.com')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

mail = Mail(app)

OWNER_EMAIL = os.environ.get('MAIL_USERNAME', 'kiruifelix03@gmail.com')
WHATSAPP_NUMBER = '+254700000000'   # ← UPDATE WITH YOUR REAL NUMBER
PHONE_NUMBER = '+254700000000'      # ← UPDATE WITH YOUR REAL NUMBER

# ── Projects data ───────────────────────────────────────────────────────────
PROJECTS = [
    {
        'title': 'CVForge AI',
        'description': 'A high-converting multi-tenant SaaS CV builder powered by Gemini AI. Users upload unstructured resumes, and the core processing engine instantly parses, cleans, and structuralizes data into a beautiful, ATS-optimized downloadable PDF. Complete with automated M-Pesa STK Push payment logic, robust authentication tiers, and a comprehensive administrator analytics panel.',
        'tags': ['Flask', 'Gemini AI', 'M-Pesa STK', 'PostgreSQL', 'PDF Generation', 'SaaS Architecture'],
        'url': '#',
        'featured': True,
    },
    {
        'title': 'Arval Blog News',
        'description': 'A premium Kenyan current affairs and political journalism platform completely engineered for organic reach. Features full Google News validation integration, comprehensive automated content refactoring utilizing LLMs, automated social syndication to X (Twitter), and advanced IndexNow configurations for instant engine indexing.',
        'tags': ['Flask', 'MySQL', 'Technical SEO', 'PythonAnywhere', 'Schema.org', 'AI Content Rewrite'],
        'url': 'https://arvalblognews.online',
        'featured': True,
    },
    {
        'title': 'High-Yield SEO & Schema Implementation',
        'description': 'Transformed an unindexed Flask news footprint into a highly authoritative, Google News approved platform. Designed custom NewsArticle, BlogPosting, and LocalBusiness schema collections, generated dynamic machine-readable feeds (RSS, Atom, Sitemap), and set up strict llms.txt definitions for cutting-edge AI crawlers.',
        'tags': ['Technical SEO', 'Schema.org', 'Google News', 'Flask', 'AI Crawlers Optimization'],
        'url': '#',
        'featured': False,
    },
]

# ── Pricing plans ─────────────────────────────────────────────────────────────
PLANS = [
    {
        'name': 'Starter (MVP & Landing Tiers)',
        'price': '$249',
        'period': 'one-time investment',
        'description': 'Establish market authority immediately. No low-grade visual templates, no slow builders you can\'t scale. Clean, hand-coded, raw speed performance.',
        'features': [
            'Up to 5-page custom structural design',
            'Ultra-fast mobile-first design (Core Web Vitals Optimized)',
            'Secure contact form with asynchronous AJAX email delivery',
            'Full structural semantic on-page SEO layout',
            'Zero-downtime deployment setup on your preferred domain',
            '30 days of comprehensive post-launch technical support',
        ],
        'cta': 'Get Started Now',
        'highlighted': False,
    },
    {
        'name': 'Professional (SaaS & Application)',
        'price': '$499',
        'period': 'one-time investment',
        'description': 'A secure, high-scale application platform. Fully customized database systems, advanced user workflows, payment pipelines, and complete dashboard control panels.',
        'features': [
            'Custom Flask full-stack modular backend ecosystem',
            'Production-ready relational database design & optimizations',
            'Secure user authentication structure (OAuth & session managed)',
            'African & Global payment integrations (M-Pesa STK Push / Stripe)',
            'Dynamic Administrator panel to view logs, metrics, & content',
            'Full JSON-LD Schema.org automation + Google News architecture',
            '90 days of comprehensive post-launch technical support',
        ],
        'cta': 'Deploy My Product',
        'highlighted': True,
    },
    {
        'name': 'Enterprise (Custom Engineering)',
        'price': 'Custom',
        'period': 'tailored quote',
        'description': 'Complex multi-tenant architectures, deep generative AI pipelines, custom data extraction engines, or long-term dedicated software engineering architecture retainer.',
        'features': [
            'Everything included in the Professional tier',
            'Advanced generative AI feature pipelines (Gemini / OpenAI APIs)',
            'Multi-tenant SaaS workspace architectures and isolated databases',
            'DevOps pipelines, automated server configurations & live telemetry',
            'Guaranteed priority delivery timeline schedules',
            'Flexible dedicated monthly infrastructure retainers available',
        ],
        'cta': 'Schedule Technical Call',
        'highlighted': False,
    },
]


@app.route('/')
def index():
    return render_template('index.html',
                           projects=PROJECTS,
                           plans=PLANS,
                           whatsapp=WHATSAPP_NUMBER,
                           phone=PHONE_NUMBER,
                           owner_email=OWNER_EMAIL)


@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    subject = data.get('subject', 'Portfolio Inquiry').strip()
    message = data.get('message', '').strip()

    if not all([name, email, message]):
        return jsonify({'success': False, 'error': 'Please fill in all required fields to proceed.'}), 400

    try:
        # Notify owner
        owner_msg = Message(
            subject=f'[Portfolio Inbound] {subject} — from {name}',
            recipients=[OWNER_EMAIL],
            body=f"""New message received from your professional web portfolio portfolio:

Name: {name}
Email: {email}
Subject: {subject}

Message Context:
{message}
"""
        )
        mail.send(owner_msg)

        # Auto-reply to client
        reply_msg = Message(
            subject='Project Request Received — Arvine Felix',
            recipients=[email],
            body=f"""Hi {name},

Thank you for getting in touch! I have successfully received your project specifications and technical overview. I will analyze your requirements and get back to you with an initial high-level review or formal timeline options within 24 hours.

Here is a duplicate copy of the inquiry information you provided:

Subject/Project Context: {subject}
Message Context: {message}

If your requirements are highly urgent or you would like to drop a supplementary reference doc link, please click straight through to my direct channels below:
- Direct WhatsApp Channel: https://wa.me/{WHATSAPP_NUMBER.replace('+', '')}
- Professional X Feed: https://x.com/Arvinefelix
- LinkedIn: https://linkedin.com/in/arvinefelix

Best regards,

Arvine Felix
 Full-Stack Software Developer
Nairobi, Kenya
"""
        )
        mail.send(reply_msg)

        return jsonify({'success': True, 'message': "Your message has been processed successfully! I will respond within 24 hours."})

    except Exception as e:
        return jsonify({'success': False, 'error': 'An email dispatch exception occurred. Please access the instant WhatsApp link instead.'}), 500


if __name__ == '__main__':
    app.run(debug=True)

