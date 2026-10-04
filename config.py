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

# ── SITE IDENTITY (used for canonical URLs, sitemap, structured data, llms.txt) ──
# When you buy a custom domain (e.g. arvalweb.co.ke), set SITE_URL to it — see notes.
SITE_URL = os.environ.get('SITE_URL', 'https://arvineportfolio.pythonanywhere.com').rstrip('/')
SITE_NAME = 'Arval Web Solutions'
OWNER_NAME = 'Arvine Felix'
OWNER_TITLE = 'Full-Stack Web Developer'
# Bump this date whenever you meaningfully change page content (feeds sitemap <lastmod>).
CONTENT_LAST_MODIFIED = '2026-10-04'
SOCIAL_LINKS = [
    'https://x.com/Arvinefelix',
    'https://linkedin.com/in/arvinefelix',
    'https://arvalblognews.online',
]

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
        'price_value': 10000,
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
        'price_value': 15000,
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
        'price_value': None,
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




# ── SERVICES (rendered on the page AND reused in structured data / llms.txt) ───
SERVICES = [
    {'icon': '⚡', 'title': 'Custom Business Systems & Web Apps',
     'desc': 'Booking systems, dashboards, inventory tools, hospital and clinic management systems, or anything specific to how your business runs — built from scratch, not squeezed into a template.',
     'tags': ['Python', 'Flask', 'Databases', 'Secure Logins']},
    {'icon': '📈', 'title': 'SEO — Get Found on Google & AI Search',
     'desc': 'Your site set up properly so Google, Bing and AI assistants (ChatGPT, Gemini, Perplexity) can find, understand and recommend you to the people searching in Kenya.',
     'tags': ['SEO', 'Schema.org', 'Google News', 'Fast Load Times']},
    {'icon': '💳', 'title': 'M-Pesa & Card Payment Integration',
     'desc': 'Accept M-Pesa (Daraja STK Push) and card payments directly on your site or app — no manual reconciliation, instant payment confirmation.',
     'tags': ['M-Pesa STK Push', 'Secure Payments', 'Stripe']},
    {'icon': '🤖', 'title': 'Practical AI Features',
     'desc': 'AI that actually helps your customers — smart summaries, local-language support, or automated content — added where it earns its place, not as a gimmick.',
     'tags': ['Gemini AI', 'Automation']},
    {'icon': '🎨', 'title': 'Fast, Mobile-First Website Design',
     'desc': 'Most of your visitors are on their phones. Every site I build is designed mobile-first and loads in under two seconds.',
     'tags': ['Mobile-First', 'Fast Loading']},
    {'icon': '🚀', 'title': 'Hosting, Domain & Setup Included',
     'desc': 'Domain connection, hosting, and security certificates set up and handled for you — one less thing to figure out.',
     'tags': ['Hosting', 'Domain Setup', 'SSL / Security']},
]

# ── FAQ (visible on the page + FAQPage schema + llms.txt) ──────────────────────
FAQS = [
    {'q': 'How much does a website cost in Kenya?',
     'a': f"A professional business website (up to 5 pages, mobile-friendly, contact form, hosting and domain connection included) starts from {PLANS[0]['price']}. Custom web apps and business systems with logins, a database, an admin dashboard and M-Pesa payments start from {PLANS[1]['price']}. Multi-branch and enterprise systems are quoted individually."},
    {'q': 'Can you integrate M-Pesa STK Push into my website or app?',
     'a': 'Yes. I integrate the Safaricom Daraja API so customers can pay by M-Pesa STK Push straight from your site or app, with instant payment confirmation and no manual reconciliation. Card payments can be added too.'},
    {'q': 'Do you build hospital, clinic or school management systems?',
     'a': 'Yes. I build custom business systems — including management systems for clinics, hospitals, schools and shops — with secure staff logins, a database and an admin dashboard. Multi-branch and multi-location setups are supported.'},
    {'q': 'Will my website show up on Google?',
     'a': 'Every site I build is set up for search from day one: fast mobile loading, clean page structure, sitemap, structured data and Google Search Console submission. Nobody can honestly guarantee a #1 ranking, but the technical foundations that let Google and AI assistants find and understand your business are built in.'},
    {'q': 'Where are you based, and who do you work with?',
     'a': 'I am a web developer based in Nairobi, Kenya. I work with small and medium businesses, clinics, schools, churches and startups across Kenya, and work remotely with clients elsewhere.'},
    {'q': 'What happens after the site goes live?',
     'a': 'Hosting and domain connection are included, and every project comes with free post-launch support (30 days for websites, 90 days for web apps). An optional monthly retainer covers ongoing support and new features.'},
    {'q': 'How quickly will you reply and how do we start?',
     'a': 'Send a project brief through the contact form or message me on WhatsApp. I reply within 24 hours with a clear plan, price and timeline — no obligation.'},
]

