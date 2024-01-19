from flask_mail import Mail, Message
from flask import current_app, flash

mail = Mail()


def init_mail(app):
    """
    Initializes Flask-Mail with the provided Flask application instance.

    Args:
        app (Flask): The Flask application instance to configure Flask-Mail.
    """
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'scootershare7@gmail.com'
    app.config['MAIL_PASSWORD'] = 'zkho jutc yrtg rerm'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    mail.init_app(app)


def send_email(subject, receipients, body):
    """
    Sends a test email using Flask-Mail configured with the current Flask application context.
    """
    try:
        with current_app.app_context():
            msg = Message(subject=subject,
                          sender=current_app.config['MAIL_USERNAME'],
                          recipients=receipients,
                          html=body
                          )
            msg.content_type = "text/html"
            mail.send(msg)

            flash("Email sent successfully!", "success")
    except Exception as error:
        print("Email sending failed:", str(error))
