from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import config  # Import factored configurations dynamically

app = Flask(__name__)

# ── BIND INFRASTRUCTURE TO FLASK OBJECT OBJECTS ──────────────────────────────
app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = config.MAIL_DEFAULT_SENDER
app.config['SECRET_KEY'] = config.SECRET_KEY

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html',
                           projects=config.PROJECTS,
                           plans=config.PLANS,
                           whatsapp=config.WHATSAPP_NUMBER,
                           phone=config.PHONE_NUMBER,
                           owner_email=config.OWNER_EMAIL)


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
        # Notify owner channel
        owner_msg = Message(
            subject=f'[Portfolio Inbound] {subject} — from {name}',
            recipients=[config.OWNER_EMAIL],
            body=f"""New message received from your professional web portfolio:

Name: {name}
Email: {email}
Subject: {subject}

Message Context:
{message}
"""
        )
        mail.send(owner_msg)

        # Asynchronous automatic confirmation responder loop
        reply_msg = Message(
            subject='Project Request Received — Arvine Felix',
            recipients=[email],
            body=f"""Hi {name},

Thank you for getting in touch! I have successfully received your project specifications and technical overview. I will analyze your requirements and get back to you with an initial high-level review or formal timeline options within 24 hours.

Here is a duplicate copy of the inquiry information you provided:

Subject/Project Context: {subject}
Message Context: {message}

If your requirements are highly urgent or you would like to drop a supplementary reference doc link, please click straight through to my direct channels below:
- Direct WhatsApp Channel: https://wa.me/{config.WHATSAPP_NUMBER.replace('+', '')}
- Professional X Feed: https://x.com/Arvinefelix
- LinkedIn: https://linkedin.com/in/arvinefelix

Best regards,

Arvine Felix
Registered Clinical Officer & Full-Stack Software Developer
Nairobi, Kenya
"""
        )
        mail.send(reply_msg)

        return jsonify({'success': True, 'message': "Your message has been processed successfully! I will respond within 24 hours."})

    except Exception as e:
        return jsonify({'success': False, 'error': 'An email dispatch exception occurred. Please access the instant WhatsApp link instead.'}), 500


if __name__ == '__main__':
    app.run(debug=True)

