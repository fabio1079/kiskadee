import os
import datetime
import jwt
from threading import Thread

from flask import make_response, jsonify, url_for
from flask_mail import Mail, Message

from kiskadee import config
from kiskadee.api.app import kiskadee
from kiskadee.api.token import token_vefirication

kiskadee.config.update({
    'MAIL_ENABLED':
    config['mail']['MAIL_ENABLED'] == 'True',
    'MAIL_SERVER':
    config['mail']['MAIL_SERVER'],
    'MAIL_PORT':
    config['mail']['MAIL_PORT'],
    'MAIL_USERNAME':
    os.environ.get('MAIL_USERNAME'),
    'MAIL_PASSWORD':
    os.environ.get('MAIL_PASSWORD'),
    'MAIL_USE_TLS':
    config['mail']['MAIL_USE_TLS'] == 'True',
    'MAIL_USE_SSL':
    config['mail']['MAIL_USE_SSL'] == 'True',
    'EMAIL_TOKEN_SECRET_KEY':
    os.environ.get('EMAIL_TOKEN_SECRET_KEY', 'dev email token')
})

mail = Mail(kiskadee)


def send_confirmation_email(user):
    if not kiskadee.config['MAIL_ENABLED']:
        return None

    token = jwt.encode(
        {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        },
        kiskadee.config['EMAIL_TOKEN_SECRET_KEY'])

    msg = Message(
        "Kiskadee email confirmation",
        sender=kiskadee.config['MAIL_USERNAME'],
        recipients=[user.email])

    link = url_for("confirm_email", token=token, _external=True)

    msg.body = '''
    Thank you for registering on kiskadee. Now please confirm your e-mail
    or your account will be deleted from our servers in a few hours.

    Confirmation link: {}

    Now if you are receiving this email by mistake, sorry for the
    inconvenience and please just ignore this message and the account
    refers to this message will be deleted.
    '''.format(link)

    mail.send(msg)


@kiskadee.route('/users/confirm_email/<token>')
def confirm_email(token):
    vefirication = token_vefirication(token, kiskadee.config['EMAIL_TOKEN_SECRET_KEY'])

    if 'error' in vefirication:
        return make_response(jsonify(vefirication), 403)
    else:
        return make_response(jsonify({'ok': True}), 200)
