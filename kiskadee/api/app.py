"""kiskadee API."""
from flask import Flask, jsonify, abort, make_response
from flask import request
from flask_cors import CORS
from marshmallow.exceptions import ValidationError

from kiskadee.database import Database
from kiskadee.model import Package, Fetcher, Version, Analysis, User,\
        TOKEN_SECRET_KEY
from kiskadee.api.serializers import PackageSchema, FetcherSchema,\
        AnalysisSchema, UserSchema
import json
from sqlalchemy.orm import eagerload

import jwt
from functools import wraps

kiskadee = Flask(__name__)

CORS(kiskadee)


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

        try:
            data = jwt.decode(token, TOKEN_SECRET_KEY)
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({'error': 'Token expired'}), 403)
        except jwt.InvalidTokenError:
            return make_response(jsonify({'error': 'Invalid token'}), 403)

        params = dict(kwargs, token_data=data)
        return fn(*args, **params)

    return decorated

@kiskadee.route('/login', methods=['POST'])
def login():
    """Token based login

    POST /login

    Possible status code:
        - 200 Ok -> User token
        - 401 Unauthorized -> Could not log user
    """
    json_data = request.get_json()
    email, password = [json_data.get('email'), json_data.get('password')]

    if email and password:
        db_session = kiskadee_db_session()
        user = db_session.query(User).filter_by(email=email).first()

        if user is not None and user.verify_password(password):
            token = user.generate_token()
            return make_response(jsonify({'token': token}), 200)

    return make_response(jsonify({'error': 'Could not verify !'}), 401)


@kiskadee.route('/fetchers')
def index():
    """Get the list of available fetchers."""
    if request.method == 'GET':
        db_session = kiskadee_db_session()
        fetchers = db_session.query(Fetcher).all()
        fetcher_schema = FetcherSchema(many=True)
        result = fetcher_schema.dump(fetchers)
        return jsonify({'fetchers': result.data})


@kiskadee.route('/packages')
def packages():
    """Get the list of analyzed packages."""
    if request.method == 'GET':
        db_session = kiskadee_db_session()
        packages = db_session.query(Package).all()
        package_schema = PackageSchema(
            many=True,
            exclude=['versions.analysis', 'versions.package_id']
        )
        data, errors = package_schema.dump(packages)
        return jsonify({'packages': data})


@kiskadee.route('/analysis/<pkg_name>/<version>', methods=['GET'])
def package_analysis_overview(pkg_name, version):
    """Get the a analysis list of some package version."""
    db_session = kiskadee_db_session()
    package_id = (
            db_session.query(Package)
            .filter(Package.name == pkg_name).first().id
        )
    version_id = (
            db_session.query(Version)
            .filter(Version.number == version)
            .filter(Version.package_id == package_id).first().id
        )
    analysis = (
            db_session.query(Analysis)
            .options(
                eagerload(Analysis.analyzers, innerjoin=True)
            )
            .filter(Analysis.version_id == version_id)
            .all()
        )
    analysis_schema = AnalysisSchema(many=True, exclude=['raw', 'report'])
    data, errors = analysis_schema.dump(analysis)
    return jsonify(data)


@kiskadee.route(
    '/analysis/<pkg_name>/<version>/<analysis_id>/results',
    methods=['GET']
)
def analysis_results(pkg_name, version, analysis_id):
    """Get the analysis results from a specific analyzer."""
    db_session = kiskadee_db_session()
    analysis = (
            db_session.query(Analysis)
            .get(analysis_id)
        )
    analysis_schema = AnalysisSchema(only=['raw'])
    data, errors = analysis_schema.dump(analysis)
    response = data['raw']['results']
    return jsonify({'analysis_results': response})


@kiskadee.route(
    '/analysis/<pkg_name>/<version>/<analysis_id>/reports',
    methods=['GET']
)
def analysis_reports(pkg_name, version, analysis_id):
    """Get the analysis reports from a specific analyzer."""
    db_session = kiskadee_db_session()
    analysis = (
            db_session.query(Analysis)
            .get(analysis_id)
        )
    analysis_schema = AnalysisSchema(only=['report'])
    data, errors = analysis_schema.dump(analysis)
    report = data['report']
    if (report is not None) and\
        ('results' in report.keys()) and\
            report['results'] is not None:
        report['results'] = json\
            .loads(report['results'])
    return jsonify({'analysis_report': report})


@kiskadee.route('/users', methods=['GET'])
@token_required
def get_users(token_data):
    """Get the list of users

    GET /users

    Possible status code:
        - 200 Ok -> Users list
    """
    db_session = kiskadee_db_session()
    users = db_session.query(User).all()
    user_schema = UserSchema(many=True)
    result = user_schema.dump(users)

    return make_response(jsonify({'users': result.data}), 200)


@kiskadee.route('/users', methods=['POST'])
def create_user():
    """Create a new user

    POST /users

    Possible status code:
        - 201 Created -> User created
        - 400 Bad Request -> Validation error
        - 403 Forbidden -> User already exists
    """
    db_session = kiskadee_db_session()
    data = request.get_json()

    # Verify is user already exists
    if data.get('email'):
        user = db_session.query(User).filter_by(email=data.get('email')).first()

        if user is not None:
            return make_response(jsonify({'error': 'user already exists'}), 403)

    # Try to create user
    try:
        user = UserSchema.create(**data)
    except ValidationError as error:
        return make_response(jsonify({
            'error': 'Validation error',
            'validations': error.args[0]
        }), 400)

    db_session.add(user)
    db_session.commit()

    user_schema = UserSchema()
    result = user_schema.dump(user)

    return make_response(jsonify({'user': result.data}), 201)


@kiskadee.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user_data(token_data, user_id):
    """Get the user data

    GET /users/:id

    Possible status code:
        - 200 Ok -> User data
        - 404 Not Found -> User not found
    """
    db_session = kiskadee_db_session()
    user = db_session.query(User).filter_by(id=user_id).first()

    if user is None:
        return make_response(jsonify({'error': 'user not found'}), 404)

    user_schema = UserSchema()
    result = user_schema.dump(user)

    return make_response(jsonify({'user': result.data}), 200)


@kiskadee.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(token_data, user_id):
    """Updates a user

    PUT /users/:id

    Possible status code:
        - 200 Ok -> User updated
        - 400 Bad Request -> Validation error
        - 403 Forbidden -> Token user does not match to requested user
        - 404 Not Found -> User not found
    """
    db_session = kiskadee_db_session()
    user = db_session.query(User).filter_by(id=user_id).first()

    if user is None:
        return make_response(jsonify({'error': 'user not found'}), 404)

    if token_data['user_id'] != user_id:
        return make_response(jsonify({
            'error': 'token user does not match to requested user'
            }), 403)

    json_data = request.get_json()
    user_data = UserSchema().dump(user).data
    user_data.update(json_data)

    validation = UserSchema().load(user_data)

    if bool(validation.errors):
        return make_response(jsonify({
            'error': 'Validation error',
            'validations': validation.errors
        }), 400)

    password = validation.data.get('validation')
    if password is not None:
        user.hash_password(password)
        del validation.data['password']

    for (key, value) in validation.data.items():
        setattr(user, key, value)

    db_session.commit()

    result = UserSchema().dump(user)
    return make_response(jsonify({'user': result.data}), 200)


@kiskadee.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(token_data, user_id):
    """Deletes a user

    DELETE /users/:id

    Possible status code:
        - 204 No Content -> User deleted
        - 403 Forbidden -> Token user does not match to requested user
        - 404 Not Found -> User not found
    """
    db_session = kiskadee_db_session()
    user = db_session.query(User).filter_by(id=user_id).first()

    if user is None:
        return make_response(jsonify({'error': 'user not found'}), 404)

    if token_data['user_id'] != user_id:
        return make_response(jsonify({
            'error': 'token user does not match to requested user'
            }), 403)

    db_session.delete(user)
    db_session.commit()

    return make_response(jsonify({}), 204)


def kiskadee_db_session():
    """Return a kiskadee database session."""
    return Database().session


def main():
    """Initialize the kiskadee API."""
    kiskadee.run('0.0.0.0')
