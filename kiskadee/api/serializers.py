"""Provide objects to serialize the kiskadee models."""

from marshmallow import Schema, fields, validate, exceptions
from kiskadee.model import Package, Fetcher, Analysis, Version,\
        Report, Analyzer, User


class ReportsSchema(Schema):
    """Provide a serializer to the Reports model."""

    id = fields.Int()
    analysis_id = fields.Int()
    results = fields.Dict()

    def make_object(self, data):
        """Serialize a Reports object."""
        print('MAKING OBJECT FROM', data)
        return Report(**data)


class AnalyzerSchema(Schema):
    """Provide a serializer to the Analyzer model."""

    id = fields.Int()
    name = fields.Str()
    version = fields.Str()
    analysis = fields.Nested('AnalysisSchema', many=True)

    def make_object(self, data):
        """Serialize a Analyzer object."""
        print('MAKING OBJECT FRON', data)
        return Analyzer(**data)


class AnalysisSchema(Schema):
    """Provide a serializer to the Analysis model."""

    id = fields.Int()
    version_id = fields.Int()
    analyzer_id = fields.Int()
    raw = fields.Dict()
    report = fields.Nested(ReportsSchema)
    analyzers = fields.Nested(AnalyzerSchema, exclude=['analysis', 'id'])

    def make_object(self, data):
        """Serialize a Analysis object."""
        print('MAKING OBJECT FROM', data)
        return Analysis(**data)


class VersionSchema(Schema):
    """Provide a serializer to the Package model."""

    id = fields.Int()
    number = fields.Str()
    package_id = fields.Int()
    analysis = fields.Nested(AnalysisSchema, many=True)

    def make_object(self, data):
        """Serialize a Package object."""
        print('MAKING OBJECT FROM', data)
        return Version(**data)


class FetcherSchema(Schema):
    """Provide a serializer to the Fetcher model."""

    id = fields.Int()
    name = fields.Str()
    target = fields.Str()
    description = fields.Str()

    def make_object(self, data):
        """Serialize a Fetcher object."""
        print('MAKING OBJECT FROM', data)
        return Fetcher(**data)


class PackageSchema(Schema):
    """Provide a serializer to the Package model."""

    id = fields.Int()
    name = fields.Str()
    fetcher_id = fields.Int()
    versions = fields.Nested(VersionSchema, many=True)

    def make_object(self, data):
        """Serialize a Package object."""
        print('MAKING OBJECT FROM', data)
        return Package(**data)


class UserSchema(Schema):
    """Provide a serializer to the User model."""

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=4, max=255))
    email = fields.Str(
        required=True,
        validate=[validate.Email(error='Not a valid email address'),
                  validate.Length(min=4, max=255)])
    password = fields.Str(load_only=True,
                          validate=validate.Length(min=4, max=255))
    is_active = fields.Bool(default=False)

    def make_object(self, data):
        """Serialize a User object."""
        print('MAKING OBJECT FROM', data)
        return User(**data)

    @classmethod
    def create(cls, **data):
        """User factory that creates a User object without saving it.

        If the given data has errors it raises an
        marshmallow.exceptions.ValidationError, else create an User model
        and return it widthout saving.

        :data: User model attributes
        """
        validation = UserSchema().load(data)

        if bool(validation.errors):
            raise exceptions.ValidationError(validation.errors)

        password = validation.data.get('password')
        if password is not None:
            del validation.data['password']

        user = User(**validation.data)

        if password is not None:
            user.hash_password(str(password))
        else:
            raise exceptions.ValidationError({
                'password': 'Missing data for required field.'
            })

        return user