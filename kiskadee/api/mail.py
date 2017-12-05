import os
import datetime
import jwt
from threading import Thread

from flask import make_response, jsonify, url_for
from flask_mail import Mail, Message

from kiskadee import config
from kiskadee.api.app import kiskadee

kiskadee.config.update({
    'MAIL_ENABLED': config['mail']['MAIL_ENABLED'] == 'True',
    'MAIL_SERVER': config['mail']['MAIL_SERVER'],
    'MAIL_PORT': config['mail']['MAIL_PORT'],
    'MAIL_USERNAME': os.environ.get('MAIL_USERNAME'),
    'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD'),
    'MAIL_USE_TLS': config['mail']['MAIL_USE_TLS'] == 'True',
    'MAIL_USE_SSL': config['mail']['MAIL_USE_SSL'] == 'True',
    'EMAIL_TOKEN_SECRET_KEY': os.environ.get('EMAIL_TOKEN_SECRET_KEY', 'dev email token')
})

mail = Mail(kiskadee)

@kiskadee.route('/users/send_email')
def send_email():
    token = jwt.encode({
        'user_id': 123456,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
    }, kiskadee.config['EMAIL_TOKEN_SECRET_KEY'])

    msg = Message("Sera ?", sender="fabio1079@gmail.com",
                  recipients=['fabio1079@gmail.com'])
    link = url_for("confirm_email", token=token, _external=True)
    msg.body = 'MAs sera memsmo ?. Link: {}'.format(link)

    mail.send(msg)

    return make_response(jsonify({'ok': True}), 200)


@kiskadee.route('/users/confirm_email/<token>')
def confirm_email(token):
    print("=" * 80)
    print("Token: {}".format(token))
    print("=" * 80)

    try:
        jwt.decode(token, kiskadee.config['EMAIL_TOKEN_SECRET_KEY'])
        return make_response(jsonify({'ok': True}), 200)
    except jwt.ExpiredSignatureError:
        return make_response(jsonify({'error': 'Token expired'}), 403)
    except jwt.InvalidTokenError:
        return make_response(jsonify({'error': 'Invalid token'}), 403)
