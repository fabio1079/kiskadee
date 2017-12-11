import jwt
import os

from functools import wraps

from flask import request, make_response, jsonify

TOKEN_SECRET_KEY = os.getenv('TOKEN_SECRET_KEY', 'default development key')


def token_vefirication(token, verification_key):
    """
    Token verification. Given a token and its key it will return the token data
    or one of the following errors: Token expired, Invalid token.

    returns:
        {'data': ...}
        or
        {'error': 'Token expired'}
        or
        {'error': 'Invalid token'}
    """
    try:
        data = jwt.decode(token, verification_key, algorithms=['HS256'])
        return {'data': data}
    except jwt.ExpiredSignatureError:
        return {'error': 'Token expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}


def token_required(fn):
    """Token verification decorator. When applyed on a route it will
    look for the x-access-token on the request header.

    If it is valid, the the route is executed.
    Else, the token is missing or is invalid or has expired, either way
    the user receive a 403 status code when invalid.

    Possible status code:
        - 403 Forbidden ->
            "Token is missing" or "Token expired" or "Invalid token"
    """

    @wraps(fn)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return make_response(jsonify({'error': 'Token is missing'}), 403)

        vefirication = token_vefirication(token, TOKEN_SECRET_KEY)

        if 'error' in vefirication:
            return make_response(jsonify(vefirication), 403)
        else:
            params = dict(kwargs, token_data=vefirication['data'])
            return fn(*args, **params)

    return decorated