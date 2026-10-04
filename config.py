"""Runtime configuration. Secrets come from environment variables — never commit them.

On PythonAnywhere set them in the WSGI file or in a `.env` loaded there, e.g.:
    os.environ['SECRET_KEY'] = '...'
See .env.example for the full list.
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def _env(name, default=''):
    return os.environ.get(name, default)


def _flag(name, default=False):
    return _env(name, str(default)).strip().lower() in ('1', 'true', 'yes', 'on')


class Config:
    # ── Core ─────────────────────────────────────────────────────────────────
    BASE_DIR = BASE_DIR
    SECRET_KEY = _env('SECRET_KEY', 'dev-secret-key')
    ADMIN_PASSWORD = _env('ADMIN_PASSWORD')           # admin login is disabled while empty
    DB_PATH = _env('DB_PATH', os.path.join(BASE_DIR, 'projects.db'))
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = _flag('SESSION_COOKIE_SECURE', False)  # True once on HTTPS only

    # ── Mail ─────────────────────────────────────────────────────────────────
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = _env('MAIL_USERNAME', 'kiruifelix03@gmail.com')
    MAIL_PASSWORD = _env('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    OWNER_EMAIL = MAIL_USERNAME

    # ── Site identity (canonical URLs, sitemap, structured data, llms.txt) ───
    SITE_URL = _env('SITE_URL', 'https://arvineportfolio.pythonanywhere.com').rstrip('/')
    SITE_NAME = 'Arval Web Solutions'
    OWNER_NAME = 'Arvine Felix'
    OWNER_TITLE = 'Full-Stack Web Developer'
    # Bump whenever page content meaningfully changes (feeds sitemap <lastmod>).
    CONTENT_LAST_MODIFIED = '2026-10-04'
    SOCIAL_LINKS = [
        'https://x.com/Arvinefelix',
        'https://linkedin.com/in/arvinefelix',
        'https://arvalblognews.online',
    ]
    WHATSAPP_NUMBER = '+254700459966'
    PHONE_NUMBER = '+254700459966'

    # ── IntaSend payments ────────────────────────────────────────────────────
    INTASEND_SECRET_KEY = _env('INTASEND_SECRET_KEY')            # ISSecretKey_test_… / ISSecretKey_live_…
    INTASEND_PUBLISHABLE_KEY = _env('INTASEND_PUBLISHABLE_KEY')  # ISPubKey_test_… / ISPubKey_live_…
    INTASEND_TEST_MODE = _flag('INTASEND_TEST_MODE', True)       # set to false when going live
    INTASEND_WEBHOOK_CHALLENGE = _env('INTASEND_WEBHOOK_CHALLENGE')  # same string you enter in the dashboard
    PAYMENT_CURRENCY = 'KES'
    # Share of the plan price collected online. 100 = pay in full, 50 = half as a deposit.
    PAYMENT_DEPOSIT_PERCENT = max(1, min(100, int(_env('PAYMENT_DEPOSIT_PERCENT', '100') or 100)))
