"""kiskadee API."""
from flask import Flask, jsonify, abort, make_response
from flask import request
from flask_cors import CORS
from marshmallow.exceptions import ValidationError

from kiskadee.database import Database
from kiskadee.model import Package, Fetcher, Version, Analysis, User
from kiskadee.api.serializers import PackageSchema, FetcherSchema,\
        AnalysisSchema, UserSchema
import json
from sqlalchemy.orm import eagerload

kiskadee = Flask(__name__)

CORS(kiskadee)


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
def get_users():
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


@kiskadee.route('/users/<user_id>', methods=['GET'])
def get_user_data(user_id):
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


@kiskadee.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a user

    PUT /users/:id

    Possible status code:
        - 200 Ok -> User updated
        - 400 Bad Request -> Validation error
        - 404 Not Found -> User not found
    """
    db_session = kiskadee_db_session()
    user = db_session.query(User).filter_by(id=user_id).first()

    if user is None:
        return make_response(jsonify({'error': 'user not found'}), 404)

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


@kiskadee.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user

    DELETE /users/:id

    Possible status code:
        - 204 No Content -> User deleted
        - 404 Not Found -> User not found
    """
    db_session = kiskadee_db_session()
    user = db_session.query(User).filter_by(id=user_id).first()

    if user is None:
        return make_response(jsonify({'error': 'user not found'}), 404)

    db_session.delete(user)
    db_session.commit()

    return make_response(jsonify({}), 204)


def kiskadee_db_session():
    """Return a kiskadee database session."""
    return Database().session


def main():
    """Initialize the kiskadee API."""
    kiskadee.run('0.0.0.0')
