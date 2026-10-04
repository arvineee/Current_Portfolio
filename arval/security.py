"""Security headers, robots hints for private paths, and a cross-site guard for admin POSTs."""
from urllib.parse import urlparse

from flask import abort, request

PRIVATE_PREFIXES = ('/admin', '/checkout', '/pay', '/webhooks')

CSP = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline'; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src 'self' https://fonts.gstatic.com; "
    "img-src 'self' data: https:; "
    "connect-src 'self'; "
    "frame-ancestors 'none';"
)


def register(app):
    @app.before_request
    def reject_cross_site_admin_posts():
        """Defence in depth on top of SameSite=Lax: an admin POST must come from our own host."""
        if request.method == 'POST' and request.path.startswith('/admin'):
            origin = request.headers.get('Origin') or request.referrer
            if origin and urlparse(origin).netloc != request.host:
                abort(403)

    @app.after_request
    def set_security_headers(response):
        response.headers['Content-Security-Policy'] = CSP
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        if request.path.startswith(PRIVATE_PREFIXES):
            response.headers['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
        if request.path in ('/sitemap.xml', '/robots.txt'):
            response.headers['Cache-Control'] = 'public, max-age=3600'
        return response
