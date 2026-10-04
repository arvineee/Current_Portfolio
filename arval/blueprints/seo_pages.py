"""Machine-facing pages: robots.txt, sitemap.xml, llms.txt and the Google verification file."""
from flask import Blueprint, current_app, render_template

from config import Config
from arval.services import catalog, seo

bp = Blueprint('seo_pages', __name__)


@bp.route('/google8caacc303a714c4c.html')
def google_verify():
    return render_template('google8caacc303a714c4c.html')


@bp.route('/robots.txt')
def robots():
    # One group for everyone (search engines and AI crawlers): public pages open, private closed.
    lines = ['User-agent: *', 'Allow: /',
             'Disallow: /admin', 'Disallow: /checkout', 'Disallow: /pay', 'Disallow: /webhooks',
             '', f'Sitemap: {Config.SITE_URL}/sitemap.xml']
    return current_app.response_class('\n'.join(lines) + '\n', mimetype='text/plain')


@bp.route('/sitemap.xml')
def sitemap():
    base, lastmod = Config.SITE_URL, Config.CONTENT_LAST_MODIFIED
    urls = [
        {'loc': f'{base}/', 'changefreq': 'weekly', 'priority': '1.0', 'image': f'{base}/static/AF.jpg'},
        {'loc': f'{base}/contact', 'changefreq': 'monthly', 'priority': '0.8'},
    ]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for u in urls:
        img = (f"<image:image><image:loc>{u['image']}</image:loc></image:image>"
               if u.get('image') else '')
        xml.append(f"<url><loc>{u['loc']}</loc><lastmod>{lastmod}</lastmod>"
                   f"<changefreq>{u['changefreq']}</changefreq><priority>{u['priority']}</priority>{img}</url>")
    xml.append('</urlset>')
    return current_app.response_class('\n'.join(xml), mimetype='application/xml')


@bp.route('/llms.txt')
def llms_txt():
    """Plain-text briefing for AI assistants / answer engines."""
    offer, plans, _ = catalog.offer_context()
    return current_app.response_class(seo.build_llms_txt(plans, offer),
                                      mimetype='text/plain; charset=utf-8')
