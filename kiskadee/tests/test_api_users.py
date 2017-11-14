import json
import unittest
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch

import kiskadee
import kiskadee.api.app

from kiskadee.model import User
from kiskadee.api.serializers import UserSchema

def mock_hash_password(self, password):
    """Mock for User model hash_password method.
    It is too slow for the tests.
    """
    self.password_hash = str(password)


class ApiUsersTestCase(unittest.TestCase):

    def setUp(self):
        kiskadee.api.app.kiskadee.testing = True
        self.engine = kiskadee.database.Database('db_test').engine
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.app = kiskadee.api.app.kiskadee.test_client()

        kiskadee.model.Base.metadata.create_all(self.engine)
        self._setup_mock_users()

    @patch.object(User, 'hash_password', mock_hash_password)
    def _setup_mock_users(self):
        mock_users_data = [
            {'name': 'test 1', 'email': 'test@user1.com', 'password': 'test'},
            {'name': 'test 2', 'email': 'test@user2.com', 'password': 'test'},
            {'name': 'test 3', 'email': 'test@user3.com', 'password': 'test'}
        ]

        for mock_data in mock_users_data:
            user = UserSchema.create(**mock_data)
            self.session.add(user)

        self.session.commit()

    def tearDown(self):
        self.session.close()
        kiskadee.model.Base.metadata.drop_all()

    # GET /users -> 200 ok
    def test_get_users(self):
        def mock_kiskadee_db_session():
            return self.session

        kiskadee.api.app.kiskadee_db_session = mock_kiskadee_db_session

        user = self.session.query(User).first()
        user_token = user.generate_token()

        response = self.app.get("/users",
                                headers={'x-access-token': user_token})
        data = json.loads(response.data.decode("utf-8"))
        total_users_count = self.session.query(User).count()

        self.assertIn("users", data)
        self.assertEqual(len(data['users']), total_users_count)
        self.assertEqual(200, response.status_code)

        # no password field is given
        user = data['users'][0]
        self.assertIsNone(user.get('password'))
        self.assertIsNone(user.get('password_hash'))


    # POST /users -> 201 created
    @patch.object(User, 'hash_password', mock_hash_password)
    def test_successful_create_user(self):
        def mock_kiskadee_db_session():
            return self.session

        kiskadee.api.app.kiskadee_db_session = mock_kiskadee_db_session

        new_user_data = {
            'name': 'new user',
            'email': 'new@user.com',
            'password': 'new user'
        }

        total_users_before_creation = self.session.query(User).count()
        response = self.app.post("/users",
                                 data=json.dumps(new_user_data),
                                 content_type='application/json')
        total_users_after_creation = self.session.query(User).count()

        data = json.loads(response.data.decode("utf-8"))

        self.assertIn("user", data)
        self.assertEqual(total_users_after_creation, total_users_before_creation + 1)
        self.assertEqual(data['user']['email'], new_user_data['email'])
        self.assertEqual(201, response.status_code)

    # POST /users -> 400 Bad Request
    def test_missing_arguments_create_user(self):
        def mock_kiskadee_db_session():
            return self.session

        kiskadee.api.app.kiskadee_db_session = mock_kiskadee_db_session

        new_user_data = {
            'name': 'new user',
            'password': 'new user'
        }

        total_users_before_creation = self.session.query(User).count()
        response = self.app.post("/users",
                                 data=json.dumps(new_user_data),
                                 content_type='application/json')
        total_users_after_creation = self.session.query(User).count()

        data = json.loads(response.data.decode("utf-8"))

        self.assertIn("error", data)
        self.assertIn("validations", data)
        self.assertEqual(total_users_after_creation, total_users_before_creation)
        self.assertEqual(data['error'], 'Validation error')
        self.assertEqual(data['validations']['email'][0],
                         'Missing data for required field.')
        self.assertEqual(400, response.status_code)

    # POST /users -> 403 Forbidden
    def test_already_exists_create_user(self):
        def mock_kiskadee_db_session():
            return self.session

        kiskadee.api.app.kiskadee_db_session = mock_kiskadee_db_session

        new_user_data = {
            'name': 'new user',
            'password': 'new user',
            'email': 'test@user1.com'
        }

        total_users_before_creation = self.session.query(User).count()
        response = self.app.post("/users",
                                 data=json.dumps(new_user_data),
                                 content_type='application/json')
        total_users_after_creation = self.session.query(User).count()

        data = json.loads(response.data.decode("utf-8"))

        self.assertIn("error", data)
        self.assertEqual(total_users_after_creation, total_users_before_creation)
        self.assertEqual(data['error'], 'user already exists')
        self.assertEqual(403, response.status_code)

    # GET /users/:id -> 200 ok
    def test_get_user_data(self):
        def mock_kiskadee_db_session():
            return self.session

        kiskadee.api.app.kiskadee_db_session = mock_kiskadee_db_session

        user = self.session.query(User).first()

        response = self.app.get("/users/%d" % user.id)
        data = json.loads(response.data.decode("utf-8"))

        self.assertIn("user", data)
        self.assertEqual(data['user']['email'], user.email)
        self.assertEqual(200, response.status_code)

        # no password field is given
        self.assertIsNone(data['user'].get('password'))
        self.assertIsNone(data['user'].get('password_hash'))

    # GET /users/:id -> 404 Not Found
    def test_not_found_get_user_data(self):
        def mock_kiskadee_db_session():
            return self.session

        kiskadee.api.app.kiskadee_db_session = mock_kiskadee_db_session

        response = self.app.get("/users/%d" % 123456789)
        data = json.loads(response.data.decode("utf-8"))

        self.assertIn("error", data)
        self.assertEqual(data['error'], 'user not found')
        self.assertEqual(404, response.status_code)

    # PUT /users/:id -> 200 ok
    @patch.object(User, 'hash_password', mock_hash_password)
    def test_successful_update_user(self):
        def mock_kiskadee_db_session():
            return self.session

        kiskadee.api.app.kiskadee_db_session = mock_kiskadee_db_session

        user = self.session.query(User).first()
        response = self.app.put("/users/{}".format(user.id),
                                 data=json.dumps({'email': 'another@email.com',
                                                  'password': 'password'}),
                                 content_type='application/json')

        data = json.loads(response.data.decode("utf-8"))

        self.assertIn("user", data)
        self.assertEqual(data['user']['id'], user.id)
        self.assertEqual(data['user']['email'], 'another@email.com')
        self.assertEqual(200, response.status_code)

        updated_user = self.session.query(User).filter_by(id=user.id).first()

        self.assertEqual(user.id, updated_user.id)
        self.assertEqual(user.password_hash, updated_user.password_hash)
        self.assertEqual(updated_user.email, 'another@email.com')

    # PUT /users/:id -> 200 ok
    @patch.object(User, 'hash_password', mock_hash_password)
    def test_ignores_password_hash_on_ajax_update_user(self):
        def mock_kiskadee_db_session():
            return self.session

        kiskadee.api.app.kiskadee_db_session = mock_kiskadee_db_session

        user = self.session.query(User).first()
        response = self.app.put("/users/{}".format(user.id),
                                 data=json.dumps({'password_hash': 'ignome_me'}),
                                 content_type='application/json')

        data = json.loads(response.data.decode("utf-8"))

        self.assertIn("user", data)
        self.assertEqual(data['user']['id'], user.id)
        self.assertEqual(200, response.status_code)

        updated_user = self.session.query(User).filter_by(id=user.id).first()

        self.assertNotEqual(updated_user.password_hash, 'ignome_me')
        self.assertEqual(updated_user.password_hash, user.password_hash)

    # PUT /users/:id -> 400 Bad Request
    @patch.object(User, 'hash_password', mock_hash_password)
    def test_validation_errors_on_update_user(self):
        def mock_kiskadee_db_session():
            return self.session

        kiskadee.api.app.kiskadee_db_session = mock_kiskadee_db_session

        user = self.session.query(User).first()
        response = self.app.put("/users/{}".format(user.id),
                                 data=json.dumps({'password': 'foo',
                                                  'email': 'not an email'}),
                                 content_type='application/json')

        data = json.loads(response.data.decode("utf-8"))

        self.assertIn("error", data)
        self.assertIn("validations", data)
        self.assertEqual(data['error'], 'Validation error')
        self.assertEqual(data['validations']['email'][0],
                         'Not a valid email address')
        self.assertEqual(data['validations']['password'][0],
                         'Length must be between 4 and 255.')
        self.assertEqual(400, response.status_code)

        updated_user = self.session.query(User).filter_by(id=user.id).first()

        self.assertNotEqual(updated_user.email, 'not an email')


    # PUT /users/:id -> 404 Not Found
    def test_not_found_update_user(self):
        def mock_kiskadee_db_session():
            return self.session

        kiskadee.api.app.kiskadee_db_session = mock_kiskadee_db_session

        response = self.app.put("/users/{}".format(123456789),
                                 data=json.dumps({'password': 'not found ?'}),
                                 content_type='application/json')

        data = json.loads(response.data.decode("utf-8"))

        self.assertIn("error", data)
        self.assertEqual(data['error'], 'user not found')
        self.assertEqual(404, response.status_code)

    # DELETE /users/:id -> 204 No Content
    def test_successful_delete_user(self):
        def mock_kiskadee_db_session():
            return self.session

        kiskadee.api.app.kiskadee_db_session = mock_kiskadee_db_session

        user = self.session.query(User).first()

        response = self.app.delete("/users/{}".format(user.id))

        self.assertEqual(response.data, b'')
        self.assertEqual(204, response.status_code)

        deleted_user = self.session.query(User).filter_by(id=user.id).first()

        self.assertIsNone(deleted_user)

    # DELETE /users/:id -> 404 Not Found
    def test_not_found_delete_user(self):
        def mock_kiskadee_db_session():
            return self.session

        kiskadee.api.app.kiskadee_db_session = mock_kiskadee_db_session

        response = self.app.delete("/users/{}".format(123456789))

        data = json.loads(response.data.decode("utf-8"))

        self.assertIn("error", data)
        self.assertEqual(data['error'], 'user not found')
        self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    unittest.main()
