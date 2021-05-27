import json
import bcrypt

from user.models  import User

from django.test import TestCase, Client

class UserSignUpTest(TestCase):
    def setUp(self):
        User.objects.create(
                email        = 'abc@gmail.com',
                password     = '123456789',
                first_name   = 'test_user_first_name',
                last_name    = 'test_user_last_name',
                sex          = 'M',
                birthday     = '0000-00-00',
                phone_number = 1012345678
            )

    def tearDown(self):
        User.objects.all().delete()

    def test_user_post_view(self):
        client   = Client()
        user     = {
                    'email'        : 'abcd@gmail.com',
                    'password'     : '1234567891',
                    'first_name'   : 'test_user_first1_name',
                    'last_name'    : 'test_user_last1_name',
                    'sex'          : 'M',
                    'birthday'     : '0000-00-00',
                    'phone_number' : 1043215678
                    }
        response = client.post('/user/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {
                'message' : 'SUCCESS'
            }
        )

    def test_user_post_duplicated_name(self):
        client = Client()
        user = {
                    'email'        : 'abcd@abc.com',
                    'password'     : '123456789',
                    'first_name'   : 'test_user_first_name',
                    'last_name'    : 'test_user_last_name',
                    'sex'          : 'M',
                    'birthday'     : '0000-00-00',
                    'phone_number' : 1012345479
                }
        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'DUPLICATE NAME'
            }
        )

    def test_user_post_duplicated_email(self):
        client = Client()
        user = {
                    'email'        : 'abc@gmail.com',
                    'password'     : '12345678',
                    'first_name'   : 'test_user_first_name',
                    'last_name'    : 'test_last_name',
                    'sex'          : 'M',
                    'birthday'     : '0000-00-00',
                    'phone_number' : 101363587
                }
        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'DUPLICATE EMAIL'
            }
        )

    def test_user_post_duplicated_phone_number(self):
        client = Client()
        user = {
                    'email'        : 'abcdc@gmail.com',
                    'password'     : '12345678',
                    'first_name'   : 'test_user_first_name',
                    'last_name'    : 'test_last_name',
                    'sex'          : 'M',
                    'birthday'     : '0000-00-00',
                    'phone_number' : 1012345678
                }
        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'DUPLICATE PHONE_NUMBER'
            }
        )

    def test_user_post_invalid_password(self):
        client = Client()
        user = {
                    'email'        : 'dnstks0204@gmail.com',
                    'password'     : '12348',
                    'first_name'   : 'test_user_first_name',
                    'last_name'    : 'test_last_name',
                    'sex'          : 'M',
                    'birthday'     : '0000-00-00',
                    'phone_number' : 101363587
                }
        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'INVALID PASSWORD'
            }
        )

    def test_user_post_invalid_email(self):
        client = Client()
        user = {
                    'email'        : 'dnstks0204gmail.com',
                    'password'     : '12348',
                    'first_name'   : 'test_user_first_name',
                    'last_name'    : 'test_last_name',
                    'sex'          : 'M',
                    'birthday'     : '0000-00-00',
                    'phone_number' : 101363587
                }
        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'INVALID EMAIL'
            }
        )

    def test_user_post_invalid_phone_number(self):
        client = Client()
        user = {
                    'email'        : '0204@gmail.com',
                    'password'     : '1234821239',
                    'first_name'   : 'test_user_first_name',
                    'last_name'    : 'test_last_name',
                    'sex'          : 'M',
                    'birthday'     : '0000-00-00',
                    'phone_number' : 1013635871332321
                }
        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'INVALID PHONE NUMBER'
            }
        )

class UserSignInTest(TestCase):
    def setUp(self):
        password         = "12345678"
        hashed_password  = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        User.objects.create(
                email        = 'abc@gmail.com',
                password     = hashed_password,
                first_name   = 'test_user_first_name',
                last_name    = 'test_user_last_name',
                sex          = 'M',
                is_auth      = True,
                birthday     = '0000-00-00',
                phone_number = 1012345678
            )

    def tearDown(self):
        User.objects.all().delete()

    def test_login_post_invalid_user(self):
        client   = Client()
        user     = {
                    "email"        : "abc@gmail.com",
                    "password"     : "123456789",
                    "is_auth"      : True
                    }
        
        response = client.post('/user/signin', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 
            {
                'message' : 'INVALID_USER'
            }
        )
