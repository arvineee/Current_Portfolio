"""Arval Web Solutions — application factory."""
import logging

from flask import Flask

import content
from config import Config
from arval import database, security
from arval.blueprints import admin, payments, public, seo_pages
from arval.extensions import mail


def create_app():
    app = Flask(__name__,
                template_folder=f'{Config.BASE_DIR}/templates',
                static_folder=f'{Config.BASE_DIR}/static')
    app.config.from_object(Config)

    if Config.SECRET_KEY == 'dev-secret-key':
        logging.getLogger(__name__).warning(
            'SECRET_KEY is the insecure default — set the SECRET_KEY environment variable.')

    mail.init_app(app)
    database.init_db(Config.DB_PATH)
    security.register(app)

    @app.context_processor
    def site_globals():
        """Available in every template."""
        return {
            'site_url': Config.SITE_URL,
            'whatsapp': Config.WHATSAPP_NUMBER,
            'phone': Config.PHONE_NUMBER,
            'owner_email': Config.OWNER_EMAIL,
            'payments_enabled': payments.payments_enabled(),
        }

    for blueprint in (public.bp, seo_pages.bp, payments.bp, admin.bp):
        app.register_blueprint(blueprint)
    return app
