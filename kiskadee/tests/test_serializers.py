import unittest
from marshmallow.exceptions import ValidationError

from kiskadee.api.serializers import UserSchema, User


class SerializersTestCase(unittest.TestCase):

    def test_UserSchema_validates_user_data(self):
        wrong_data = {'name': 'foo', 'email': 'foo', 'password': 'foo'}
        validation = UserSchema().load(wrong_data)

        self.assertTrue(validation.errors)
        self.assertEqual(validation.errors['name'][0],
                         'Length must be between 4 and 255.')
        self.assertEqual(validation.errors['email'][0],
                         'Not a valid email address')
        self.assertEqual(validation.errors['email'][1],
                         'Length must be between 4 and 255.')
        self.assertEqual(validation.errors['password'][0],
                         'Length must be between 4 and 255.')

        validation = UserSchema().load({})

        self.assertEqual(validation.errors['name'][0],
                         'Missing data for required field.')

        self.assertEqual(validation.errors['email'][0],
                         'Missing data for required field.')

    def test_UserSchema_create_a_user_instance(self):
        data = {'name': 'Test', 'email': 'test@email.com', 'password': 'test'}
        user = UserSchema.create(**data)

        self.assertIsInstance(user, User)
        self.assertNotEqual(user.password_hash, 'test')
        self.assertGreater(len(user.password_hash), 100)

    def test_UserSchema_raise_ValidationError_if_data_is_invalid(self):
        with self.assertRaises(ValidationError) as context:
            data = {}
            UserSchema.create(**data)

        errors = context.exception.args[0]
        self.assertIsInstance(context.exception, ValidationError)
        self.assertEqual(errors['name'][0],
                         'Missing data for required field.')
        self.assertEqual(errors['email'][0],
                         'Missing data for required field.')


if __name__ == '__main__':
    unittest.main()