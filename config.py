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

# ── BRANDING & BUSINESS COMMUNICATIONS ────────────────────────────────────────
WHATSAPP_NUMBER = '+254700459966'
PHONE_NUMBER = '+254700459966'

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

# ── PRICING — WHAT THE CLIENT GETS, IN PLAIN TERMS ────────────────────────────
# NOTE: figures below are a starting placeholder — update to your real rates.
PLANS = [
    {
        'name': 'Website / Landing Page',
        'price': 'KES 10,000',
        'period': 'one-time',
        'description': 'A clean, fast, mobile-friendly website that makes your business look credible online and brings in enquiries — for shops, clinics, schools, churches, and small businesses.',
        'features': [
            'Up to 5 pages, designed around your business',
            'Loads fast on phones — where most of your customers are',
            'Contact form that emails you instantly',
            'Set up to show up when people search for you on Google',
            'Hosting and domain connection included',
            '30 days of free support after launch',
        ],
        'cta': 'Get Started Now',
        'highlighted': False,
    },
    {
        'name': 'Web App / Business System',
        'price': 'KES 15,000',
        'period': 'one-time (from)',
        'description': "A custom system built around how your business actually runs — logins, a database, an admin dashboard, and M-Pesa payments if you need them. The kind of tool you'd otherwise pay a monthly SaaS subscription for, except it's yours.",
        'features': [
            'Custom-built backend, not a rented template',
            'Secure logins for staff, customers, or both',
            'M-Pesa (STK Push) or card payments built in',
            "An admin dashboard to see what's happening at a glance",
            'Built to grow with you as your business grows',
            '90 days of free support after launch',
        ],
        'cta': 'Start My Project',
        'highlighted': True,
    },
    {
        'name': 'Enterprise / Ongoing Partner',
        'price': 'Custom',
        'period': 'tailored quote',
        'description': 'For multi-branch operations, hospitals, or businesses that need something built specifically for them — plus ongoing help keeping it running and improving over time.',
        'features': [
            'Everything in the Web App tier',
            'AI features where they genuinely help (not just for show)',
            'Multi-branch / multi-location support',
            'Priority delivery timelines',
            'Optional monthly retainer for ongoing support & new features',
        ],
        'cta': 'Book a Call',
        'highlighted': False,
    },
]


