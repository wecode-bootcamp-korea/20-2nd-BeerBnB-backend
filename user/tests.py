from user.models  import User

from django.test import TestCase, Client

class UserTest(TestCase):
    def setUp(self):
        User.objects.create(
                email        = 'abc@gmail.com',
                password     = '12345678',
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
                    'email'        : 'dnstks0204@gmail.com',
                    'password'     : '12345678',
                    'first_name'   : 'test_first_name',
                    'last_name'    : 'test_last_name',
                    'sex'          : 'M',
                    'birthday'     : '0000-00-00',
                    'phone_number' : 101363587
                    }
        response = client.post('/user/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {
                'message' : 'success'
            }
        )

    def test_user_post_duplicated_name(self):
        client = Client()
        user = {
                    'email'        : 'dnstks0204@gmail.com',
                    'password'     : '12345678',
                    'first_name'   : 'test_user_first_name',
                    'last_name'    : 'test_last_name',
                    'sex'          : 'M',
                    'birthday'     : '0000-00-00',
                    'phone_number' : 101363587
                }
        response = client.post('/user/signup', json.dumps(author), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'DUPLICATED_NAME'
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
        response = client.post('/user/signup', json.dumps(author), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'DUPLICATED_EMAIL'
            }
        )

    def test_user_post_duplicated_phone_number(self):
        client = Client()
        user = {
                    'email'        : 'abc@gmail.com',
                    'password'     : '12345678',
                    'first_name'   : 'test_user_first_name',
                    'last_name'    : 'test_last_name',
                    'sex'          : 'M',
                    'birthday'     : '0000-00-00',
                    'phone_number' : 1012345678
                }
        response = client.post('/user/signup', json.dumps(author), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'DUPLICATED_PHONE_NUMBER'
            }
        )

    def test_user_post_invalid_password(self):
        client = Client()
        author = {
                    'email'        : 'dnstks0204@gmail.com',
                    'password'     : '12348',
                    'first_name'   : 'test_user_first_name',
                    'last_name'    : 'test_last_name',
                    'sex'          : 'M',
                    'birthday'     : '0000-00-00',
                    'phone_number' : 101363587
                }
        response = client.post('/user/signup', json.dumps(author), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'INVALID_PASSWORD'
            }
        )

    def test_user_post_invalid_email(self):
        client = Client()
        author = {
                    'email'        : 'dnstks0204gmail.com',
                    'password'     : '12348',
                    'first_name'   : 'test_user_first_name',
                    'last_name'    : 'test_last_name',
                    'sex'          : 'M',
                    'birthday'     : '0000-00-00',
                    'phone_number' : 101363587
                }
        response = client.post('/user/signup', json.dumps(author), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'INVALID_EMAIL'
            }
        )

    def test_user_post_invalid_phone_number(self):
        client = Client()
        author = {
                    'email'        : 'dnstks0204@gmail.com',
                    'password'     : '12348',
                    'first_name'   : 'test_user_first_name',
                    'last_name'    : 'test_last_name',
                    'sex'          : 'M',
                    'birthday'     : '0000-00-00',
                    'phone_number' : 1013635871332321
                }
        response = client.post('/user/signup', json.dumps(author), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'INVALID_PHONE_NUMBER'
            }
        )

        