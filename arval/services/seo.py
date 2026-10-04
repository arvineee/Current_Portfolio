"""Structured data (JSON-LD) and llms.txt builders.

Everything is generated from content.py and config.py so the page, the schema and the AI
manifest can never drift apart.
"""
import content
from config import Config as cfg

SITE = cfg.SITE_URL
BUSINESS_ID = f'{SITE}/#business'
PERSON_ID = f'{SITE}/#person'
WEBSITE_ID = f'{SITE}/#website'
LOGO_URL = f'{SITE}/static/AF.jpg'

KNOWS_ABOUT = [
    'Web development', 'Website design', 'Python', 'Flask', 'M-Pesa Daraja API',
    'Search engine optimization', 'Schema.org structured data', 'Business management systems',
    'Hospital management systems', 'SaaS development', 'Generative AI integration',
]


def _offers(plans, offer):
    offers = []
    for plan in plans:
        offer_node = {
            '@type': 'Offer',
            'name': plan['name'],
            'description': plan['description'],
            'priceCurrency': 'KES',
            'availability': 'https://schema.org/InStock',
            'url': f'{SITE}/#pricing',
            'itemOffered': {'@type': 'Service', 'name': plan['name'], 'provider': {'@id': BUSINESS_ID}},
        }
        if plan.get('price_value'):
            current = plan.get('sale_price_value') or plan['price_value']
            offer_node['priceSpecification'] = {
                '@type': 'PriceSpecification',
                'minPrice': current,
                'priceCurrency': 'KES',
            }
            if plan.get('sale_price_value') and offer:
                offer_node['priceValidUntil'] = offer['ends_at_date']
        offers.append(offer_node)
    return offers


def build_home_schema(plans=None, offer=None):
    plans = plans or content.PLANS
    prices = [p.get('sale_price_value') or p['price_value'] for p in plans if p.get('price_value')]
    return {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'WebSite',
                '@id': WEBSITE_ID,
                'url': f'{SITE}/',
                'name': cfg.SITE_NAME,
                'inLanguage': 'en-KE',
                'publisher': {'@id': BUSINESS_ID},
            },
            {
                '@type': 'WebPage',
                '@id': f'{SITE}/#webpage',
                'url': f'{SITE}/',
                'name': 'Web Developer in Nairobi, Kenya — Websites, Web Apps & M-Pesa Integration',
                'isPartOf': {'@id': WEBSITE_ID},
                'about': {'@id': BUSINESS_ID},
                'primaryImageOfPage': {'@type': 'ImageObject', 'url': LOGO_URL},
                'dateModified': cfg.CONTENT_LAST_MODIFIED,
                'inLanguage': 'en-KE',
            },
            {
                '@type': 'Person',
                '@id': PERSON_ID,
                'name': cfg.OWNER_NAME,
                'jobTitle': cfg.OWNER_TITLE,
                'url': f'{SITE}/',
                'image': LOGO_URL,
                'worksFor': {'@id': BUSINESS_ID},
                'homeLocation': {'@type': 'City', 'name': 'Nairobi'},
                'nationality': {'@type': 'Country', 'name': 'Kenya'},
                'knowsAbout': KNOWS_ABOUT,
                'sameAs': cfg.SOCIAL_LINKS,
            },
            {
                '@type': ['ProfessionalService', 'LocalBusiness'],
                '@id': BUSINESS_ID,
                'name': cfg.SITE_NAME,
                'alternateName': [f'{cfg.OWNER_NAME} Web Developer', 'Arval Web Solutions Nairobi'],
                'description': (
                    'Web developer in Nairobi, Kenya building fast, mobile-first websites, custom web apps '
                    'and business systems with M-Pesa payment integration, SEO and AI features.'
                ),
                'url': f'{SITE}/',
                'logo': {'@type': 'ImageObject', 'url': LOGO_URL},
                'image': LOGO_URL,
                'telephone': cfg.PHONE_NUMBER,
                'email': cfg.OWNER_EMAIL,
                'priceRange': f'From KES {min(prices):,}',
                'currenciesAccepted': 'KES',
                'paymentAccepted': 'M-Pesa, Card',
                'address': {
                    '@type': 'PostalAddress',
                    'addressLocality': 'Nairobi',
                    'addressRegion': 'Nairobi County',
                    'addressCountry': 'KE',
                },
                'geo': {'@type': 'GeoCoordinates', 'latitude': -1.2921, 'longitude': 36.8219},
                'areaServed': [
                    {'@type': 'Country', 'name': 'Kenya'},
                    {'@type': 'City', 'name': 'Nairobi'},
                ],
                'founder': {'@id': PERSON_ID},
                'knowsAbout': KNOWS_ABOUT,
                'serviceType': [s['title'] for s in content.SERVICES],
                'contactPoint': {
                    '@type': 'ContactPoint',
                    'contactType': 'sales',
                    'telephone': cfg.WHATSAPP_NUMBER,
                    'email': cfg.OWNER_EMAIL,
                    'availableLanguage': ['English'],
                    'areaServed': 'KE',
                },
                'hasOfferCatalog': {
                    '@type': 'OfferCatalog',
                    'name': 'Web development services and pricing',
                    'itemListElement': _offers(plans, offer),
                },
                'sameAs': cfg.SOCIAL_LINKS,
            },
            {
                '@type': 'FAQPage',
                '@id': f'{SITE}/#faq',
                'mainEntity': [
                    {'@type': 'Question', 'name': f['q'],
                     'acceptedAnswer': {'@type': 'Answer', 'text': f['a']}}
                    for f in content.FAQS
                ],
            },
        ],
    }


def build_contact_schema():
    return {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'ContactPage',
                '@id': f'{SITE}/contact#webpage',
                'url': f'{SITE}/contact',
                'name': 'Contact a Web Developer in Nairobi — Free Website Quote',
                'isPartOf': {'@id': WEBSITE_ID},
                'about': {'@id': BUSINESS_ID},
                'inLanguage': 'en-KE',
                'breadcrumb': {'@id': f'{SITE}/contact#breadcrumb'},
            },
            {
                '@type': 'BreadcrumbList',
                '@id': f'{SITE}/contact#breadcrumb',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': f'{SITE}/'},
                    {'@type': 'ListItem', 'position': 2, 'name': 'Contact', 'item': f'{SITE}/contact'},
                ],
            },
        ],
    }


def build_llms_txt(plans=None, offer=None):
    """llms.txt — a plain-markdown briefing for AI assistants and answer engines."""
    L = []
    L.append(f'# {cfg.SITE_NAME}')
    L.append('')
    L.append(
        f'> {cfg.SITE_NAME} is the web development practice of {cfg.OWNER_NAME}, a full-stack web '
        'developer based in Nairobi, Kenya. It builds fast mobile-first websites, custom web apps and '
        'business systems (including hospital/clinic management systems), M-Pesa (Daraja STK Push) payment '
        'integration, technical SEO and practical AI features for businesses in Kenya and remotely worldwide.'
    )
    L.append('')
    L.append('## Key facts')
    L.append(f'- Name: {cfg.OWNER_NAME} ({cfg.OWNER_TITLE})')
    L.append('- Location: Nairobi, Kenya')
    L.append('- Stack: Python, Flask, SQLAlchemy, MySQL/PostgreSQL, Tailwind CSS, HTMX/Alpine.js, M-Pesa Daraja API, Gemini AI')
    L.append('- Reply time: within 24 hours with a clear plan, price and timeline')
    L.append(f'- Website: {SITE}/')
    L.append(f'- Contact form: {SITE}/contact')
    L.append(f'- Email: {cfg.OWNER_EMAIL}')
    L.append(f'- WhatsApp: https://wa.me/{cfg.WHATSAPP_NUMBER.replace("+", "")}')
    L.append('')
    L.append('## Services')
    for s in content.SERVICES:
        L.append(f'- **{s["title"]}**: {s["desc"]}')
    L.append('')
    L.append('## Pricing (KES)')
    plans = plans or content.PLANS
    if offer:
        L.append(f'- **LIMITED OFFER: {offer["title"]}** — {offer.get("message", "")} Valid until {offer["ends_at_label"]}.')
    for p in plans:
        price = p['price']
        if p.get('sale_price'):
            price = f'{p["sale_price"]} (was {p["price"]}, {p["percent_off"]}% off)'
        L.append(f'- **{p["name"]}** — {price} ({p["period"]}): {p["description"]}')
    L.append('')
    L.append('## Live work')
    for p in content.PROJECTS:
        url = f' — {p["url"]}' if p.get('url') and p['url'] != '#' else ''
        L.append(f'- **{p["title"]}**{url}: {p["description"]}')
    L.append('')
    L.append('## Frequently asked questions')
    for f in content.FAQS:
        L.append(f'### {f["q"]}')
        L.append(f['a'])
        L.append('')
    L.append('## Links')
    for link in cfg.SOCIAL_LINKS:
        L.append(f'- {link}')
    L.append(f'- [Sitemap]({SITE}/sitemap.xml)')
    return '\n'.join(L) + '\n'
