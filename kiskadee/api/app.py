"""kiskadee API."""
from flask import Flask, jsonify
from flask import request
from flask_cors import CORS

from kiskadee.database import Database
from kiskadee.model import Package, Fetcher, Version, Analysis
from kiskadee.api.serializers import PackageSchema, FetcherSchema,\
        AnalysisSchema
import json

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
        # TODO: get the last version using sequelize
        for item in data:
            item['version'] = sorted(
                item['versions'],
                key=lambda k: k['number'],
                reverse=True
            )[0]['number'] # only the last version
            item.pop('versions', None)
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
            .filter(Analysis.version_id == version_id).all()
        )
    analysis_schema = AnalysisSchema(many=True)
    results = analysis_schema.dump(analysis)
    result_data = []
    for result in results.data:
        current_data = {
            'analyzer_id': result['analyzer_id'],
            'id': result['id'],
            'version': result['raw']['metadata']['generator']['version'],
            'name': result['raw']['metadata']['generator']['name']
        }
        result_data.append(current_data)
    return jsonify(result_data)


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
    analysis_schema = AnalysisSchema()
    results = analysis_schema.dump(analysis)
    response = results.data['raw']['results']
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
    analysis_schema = AnalysisSchema()
    results = analysis_schema.dump(analysis)
    report = results.data['report']
    if (report is not None) and\
        ('results' in report.keys()) and\
            report['results'] is not None:
        report['results'] = json\
            .loads(report['results'])
    return jsonify({'analysis_report': report})


def kiskadee_db_session():
    """Return a kiskadee database session."""
    return Database().session


def main():
    """Initialize the kiskadee API."""
    kiskadee.run('0.0.0.0')
