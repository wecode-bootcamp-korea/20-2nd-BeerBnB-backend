import json, jwt
import boto3
import io
import bcrypt
import requests

from PIL import Image
from user.models    import User
from django.test    import TestCase
from django.test    import Client
from unittest.mock  import patch, MagicMock
from my_settings    import SECRET_KEY

class SocialUserTest(TestCase):
    @patch("user.views.requests")
    def test_kakao_signin_new_user_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'id' : 1,
                    'kakao_account':{'email':'abc@gmail.com',
                                     'gender':'M',
                                     'birthday':'2021-05-31'
                                    }
                }
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorization':'token'}
        response            = client.get("/user/kakao", **headers)
        id                  = MockedResponse().json()['id']
        access_token        = jwt.encode({'id':id}, SECRET_KEY, algorithm='HS256')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        
            {
                'message': 'existing user',
                'access_token': access_token
            }
        )
                        
    @patch("user.views.requests")
    def test_kakao_signin_new_user_token_required(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'id' : 1,
                    'kakao_account':{'email':'abc@gmail.com',
                                     'gender':'M',
                                     'birthday':'2021-05-31'
                                    }
                }
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorization':''}
        response            = client.get("/user/kakao", **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'TOKEN REQUIRED'
            }
        )
    @patch("user.views.requests")
    def test_kakao_signin_new_user_email_required(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'id' : 1,
                    'kakao_account':{
                                     'gender':'M',
                                     'birthday':'2021-05-31'
                                    }
                }
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorization':'token'}
        response            = client.get("/user/kakao", **headers)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(),
            {
                'message' : 'EMAIL REQUIRED'
            }
        )

class ProfileUploadTest(TestCase):
    def setUp(self):
        password = '123456789'.encode('utf-8')
        password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

        User.objects.create(
                id           = 1,
                email        = 'abc@gmail.com',
                password     = password,
                first_name   = 'test_user_first1_name',
                last_name    = 'test_user_last1_name',
                sex          = 'M',
                birthday     = '0000-00-00',
                phone_number = 1012345678
            )
    def tearDown(self):
        User.objects.all().delete()

    def generate_photo_file(self):
        file  = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    @patch("user.views.boto3.client")
    def test_upload_success_photo(self, mocked_client):
        mocked_client = MagicMock()
        client        = Client()
        user          = User.objects.get(id = 1)
        token         = jwt.encode({'id': user.id}, SECRET_KEY, algorithm = 'HS256')
        headers       = {"HTTP_Authorization" : token}
        bucket        = "test"
        profile_file  = self.generate_photo_file()
        file_urls     = f"https://AWS_S3_CUSTOM_DOMAIN/profile/{profile_file}" 
        data          = {'profile_file':profile_file}

        user.profile_url = file_urls
        user.save()
        response = client.post('/user/upload', data, format='multipart', **headers)
        self.assertEqual(response.status_code, 200)

    @patch("user.views.boto3.client")
    def test_upload_none_token_photo(self, mocked_client):
        mocked_client = MagicMock()
        client        = Client()
        user          = User.objects.get(id = 1)
        token         = jwt.encode({'id': user.id}, SECRET_KEY, algorithm = 'HS256')
        bucket        = "test"
        profile_file  = self.generate_photo_file()
        file_urls     = f"https://AWS_S3_CUSTOM_DOMAIN/profile/{profile_file}" 
        data          = {'profile_file':profile_file}

        user.profile_url = file_urls
        user.save()
        response = client.post('/user/upload', data, format='multipart')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 
            {
                'MESSAGE' : 'NO LOGIN'
            }
        )

    @patch("user.views.boto3.client")
    def test_upload_invalid_token_photo(self, mocked_client):
        mocked_client = MagicMock()
        client        = Client()
        user          = User.objects.get(id = 1)
        token         = jwt.encode({'id': user.id}, SECRET_KEY, algorithm = 'HS256')
        headers       = {"HTTP_Authorization" : 'test_token'}
        bucket        = "test"
        profile_file  = self.generate_photo_file()
        file_urls     = f"https://AWS_S3_CUSTOM_DOMAIN/profile/{profile_file}" 
        data          = {'profile_file':profile_file}

        user.profile_url = file_urls
        user.save()
        response = client.post('/user/upload', data, format='multipart', **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'MESSAGE': 'INVALID_TOKEN'
            }
        )
    
    @patch("user.views.boto3.client")
    def test_upload_invalid_user_photo(self, mocked_client):
        mocked_client  = MagicMock()
        client         = Client()
        user           = User.objects.get(id = 1)
        test_id        = 2
        token          = jwt.encode({'id': test_id}, SECRET_KEY, algorithm = 'HS256')
        headers        = {"HTTP_Authorization" : token}
        bucket         = "test"
        profile_file   = self.generate_photo_file()
        file_urls      = f"https://AWS_S3_CUSTOM_DOMAIN/profile/{profile_file}" 
        data           = {'profile_file':profile_file}

        user.profile_url = file_urls
        user.save()
        response = client.post('/user/upload', data, format='multipart', **headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 
            {
                'MESSAGE' : 'INVALID_USER'
            }
        )

    @patch("user.views.boto3.client")
    def test_upload_key_error_photo(self, mocked_client):
        mocked_client  = MagicMock()
        client         = Client()
        user           = User.objects.get(id = 1)
        invalid_key    = 'test_key'
        token          = jwt.encode({invalid_key: user.id}, SECRET_KEY, algorithm = 'HS256')
        headers        = {"HTTP_Authorization" : token}
        bucket         = "test"
        profile_file   = self.generate_photo_file()
        file_urls      = f"https://AWS_S3_CUSTOM_DOMAIN/profile/{profile_file}" 
        data           = {'profile_file':profile_file}

        user.profile_url = file_urls
        user.save()
        response = client.post('/user/upload', data, format='multipart', **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'MESSAGE': 'KEY_ERROR'
            }
        )
        
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
                is_allowed   = True,
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
                    "is_allowed"   : True
                    }
        
        response = client.post('/user/signin', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 
            {
                'message' : 'INVALID_USER'
            }
        )
    
