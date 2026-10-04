"""Public pages: home and contact."""
from flask import Blueprint, jsonify, render_template, request

import content
from arval.services import catalog, mailer, seo
from arval.services.tracking import track_visit
from arval.repos import projects

bp = Blueprint('public', __name__)


@bp.route('/')
def index():
    track_visit()
    offer, plans, featured_plan = catalog.offer_context()
    return render_template(
        'index.html',
        projects=projects.all_projects(),
        plans=plans,
        offer=offer,
        featured_plan=featured_plan,
        services=content.SERVICES,
        faqs=content.FAQS,
        schema=seo.build_home_schema(plans, offer),
    )


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        track_visit()
        return render_template('contact.html', schema=seo.build_contact_schema())

    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip()
    subject = (data.get('subject') or 'Portfolio Inquiry').strip()
    message = (data.get('message') or '').strip()

    if not (name and email and message):
        return jsonify({'success': False, 'error': 'Please fill in all required fields.'}), 400
    try:
        mailer.send_contact_message(name, email, subject, message)
    except Exception:
        return jsonify({'success': False,
                        'error': 'Email dispatch failed. Please use WhatsApp instead.'}), 500
    return jsonify({'success': True, 'message': 'Message sent! I will respond within 24 hours.'})
