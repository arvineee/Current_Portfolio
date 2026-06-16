import os

# ── MAIL INFRASTRUCTURE CONFIGURATION ────────────────────────────────────────
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True

# Safe runtime fallback checking for system environment variables
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'kiruifelix03@gmail.com')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'your_app_password')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME', 'kiruifelix03@gmail.com')
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

OWNER_EMAIL = os.environ.get('MAIL_USERNAME', 'kiruifelix03@gmail.com')

# ── BRANDING & BUSINESS COMMUNICATIONS MATRIX ─────────────────────────────────
WHATSAPP_NUMBER = '+254700000000'   # ← UPDATE WITH YOUR REAL NUMBER
PHONE_NUMBER = '+254700000000'      # ← UPDATE WITH YOUR REAL NUMBER

# ── LIVE PRODUCTION PROJECTS PORTFOLIO DATA ──────────────────────────────────
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

# ── TRANSPARENT SERVICE INVESTMENT TIERS ─────────────────────────────────────
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

