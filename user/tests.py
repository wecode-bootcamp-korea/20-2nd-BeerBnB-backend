import json, jwt
import boto3
import io
import bcrypt
import requests
from PIL         import Image as PIL

from user.models import User, Host
from room.models import Room, Category, Image, Amenity, DisableDate, AbleTime

from django.test            import TestCase
from django.test            import Client
from django.utils.encoding  import force_bytes
from django.utils.http      import urlsafe_base64_encode
from unittest.mock          import patch, MagicMock
from my_settings            import SECRET_KEY

class AuthTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        password = '123456789'.encode('utf-8')
        password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
        User.objects.create(
                id           = 1,
                email        = 'abc@gmail.com',
                password     = password,
                first_name   = 'test_user_first_name',
                last_name    = 'test_user_last_name',
                sex          = 'M',
                birthday     = '0000-00-00',
                phone_number = 10123453278,
                is_allowed   = False,
            )
            
    def tearDown(self):
        User.objects.all().delete()

    def test_success_auth_email(self):
        client      = Client()
        user        = User.objects.get(id=1)
        uid64       = urlsafe_base64_encode(force_bytes(user.id))
        email_token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm='HS256')
        response    = client.get(f"/user/auth/{uid64}/{email_token}")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.is_allowed, True)

    def test_success_auth_email(self):
        client      = Client()
        user        = User.objects.get(id=1)
        uid64       = urlsafe_base64_encode(force_bytes(user.id))
        email_token = jwt.encode({'id':2}, SECRET_KEY, algorithm='HS256')
        response    = client.get(f"/user/auth/{uid64}/{email_token}")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'massage': 'auth fail'
            }
        )

class HostUserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        password         = "12345678"
        hashed_password  = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        
        test_user = User.objects.create(
                id           = 1,
                email        = 'abc@gmail.com',
                password     = hashed_password,
                first_name   = 'test_user_first_name',
                last_name    = 'test_user_last_name',
                sex          = 'M',
                is_allowed   = True,
                birthday     = '0000-00-00',
                phone_number = 1012345678,
            )

        test2_user = User.objects.create(
                id           = 2,
                email        = 'test2@test2.com',
                password     = password,
                first_name   = 'test_user_first2_name',
                last_name    = 'test_user_last2_name',
                sex          = 'M',
                birthday     = '0000-00-00',
                phone_number = 1012345673
            )

        test_host = Host.objects.create(
            user = test_user
        )

        category   = Category.objects.create(name="test_type")
        able_time  = AbleTime.objects.create(checkin="13:00", checkout="14:00")
        AbleTime.objects.create(checkin="14:00", checkout="15:00")
        DisableDate.objects.create(start_date="1101-10-10", end_date="1111-11-11")
        Amenity.objects.create(name="test_amenity", image="i'm url")
        Amenity.objects.create(name="test2_amenity", image="i'm url2")
        Room.objects.create(
                id           = 1,
                name         = "test1",
                min_date     = "test_date1",
                city         = "test_type1",
                category     = category,
                capacity     = "3",
                is_refund    = True,
                price        = "99999",
                latitude     =  37.4224764,
                longtitude   =  -122.0842499,
                host         = test_host,
                able_time    = able_time,
        )
    def tearDown(self):
        User.objects.all().delete()

        Category.objects.all().delete()

        Amenity.objects.all().delete()

        DisableDate.objects.all().delete()

        # AbleTime.objects.all().delete()

        Host.objects.all().delete()

        Room.objects.all().delete()

    
    def generate_photo_file_list(self):
        file_list   = []
        TEST_NUMBER = 5
        for _ in range(TEST_NUMBER):
            file  = io.BytesIO()
            image = PIL.new('RGBA', size=(100, 100), color=(155, 0, 0))
            image.save(file, 'png')
            file.name = 'test.png'
            file.seek(0)
            file_list.append(file)
        return file_list

    @patch("user.views.boto3.client")
    @patch("user.views.googlemaps.Client")
    def test_host_registrate_success(self, geoclient_requests, mocked_client):
        client    = Client()
        category  = Category.objects.get(id=1)
        amenity1  = Amenity.objects.get(id=1)
        amenity2  = Amenity.objects.get(id=2)
        
        class GmapsMockedResponse:
            def json(self):
                return [{
                        "formatted_address" : "test_address",
                                 "geometry" : {
                                 "location" : {
                                      "lat" : 37.4224764,
                                      "lng" : -122.0842499
                        }
                    }
                }]

        
        host_data = {
                    "id"          : 1,
                    "name"        : "room",
                    "min_date"    : "test_date",
                    "city"        : "test_type",
                    "category"    : "test_type",
                    "adult"       : "1",
                    "children"    : "3",
                    "is_refund"   : True,
                    "price"       : "40000",
                    "amenity"     : ["test_amenity", "test2_amenity"],
                    "address"     : "test_address"             
                }

        gmaps               = MagicMock()
        gmaps.geocode       = MagicMock(return_value= GmapsMockedResponse().json()) 
        geoclient_requests.return_value = gmaps
        user                = User.objects.get(id=1)
        room                = Room.objects.get(id=1)
        token               = jwt.encode({'id': user.id}, SECRET_KEY, algorithm = 'HS256')
        headers             = {"HTTP_Authorization": token}
        bucket              = "test"
        room_file_list      = self.generate_photo_file_list()
        file_urls_list      = [f"https://AWS_S3_CUSTOM_DOMAIN/room/{room_file}" for room_file in room_file_list]
        data                = {'room_file':room_file_list, 'room_info':json.dumps(host_data)}
            
        for file_urls in file_urls_list:
            user.profile_url = file_urls
            user.save()
        response            = client.post("/user/host", data, **headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),
            {
                'message': 'success',
                'room_id': 2
            }
        )

    @patch("user.views.boto3.client")
    @patch("user.views.googlemaps.Client")
    def test_host_registrate_success(self, geoclient_requests, mocked_client):
        client    = Client()
        category  = Category.objects.get(id=1)
        amenity1  = Amenity.objects.get(id=1)
        amenity2  = Amenity.objects.get(id=2)
        
        class GmapsMockedResponse:
            def json(self):
                return [{
                        "formatted_address" : "test_address",
                                 "geometry" : {
                                 "location" : {
                                      "lat" : 37.4224764,
                                      "lng" : -122.0842499
                        }
                    }
                }]

        
        host_data = {
                    "id"          : 1,
                    "name"        : "room",
                    "min_date"    : "test_date",
                    "city"        : "test_type",
                    "category"    : "test_type",
                    "adult"       : "1",
                    "children"    : "3",
                    "is_refund"   : True,
                    "price"       : "40000",
                    "amenity"     : [],
                    "address"     : "test_address"             
                }

        gmaps               = MagicMock()
        gmaps.geocode       = MagicMock(return_value= GmapsMockedResponse().json()) 
        geoclient_requests.return_value = gmaps
        user                = User.objects.get(id=1)
        room                = Room.objects.get(id=1)
        token               = jwt.encode({'id': user.id}, SECRET_KEY, algorithm = 'HS256')
        headers             = {"HTTP_Authorization": token}
        bucket              = "test"
        room_file_list      = self.generate_photo_file_list()
        file_urls_list      = [f"https://AWS_S3_CUSTOM_DOMAIN/room/{room_file}" for room_file in room_file_list]
        data                = {'room_file':room_file_list, 'room_info':json.dumps(host_data)}
            
        for file_urls in file_urls_list:
            user.profile_url = file_urls
            user.save()
        response            = client.post("/user/host", data, **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'none send amenity'
            }
        )

    
    @patch("user.views.boto3.client")
    @patch("user.views.googlemaps.Client")
    def test_host_registrate_none_room_info(self, geoclient_requests, mocked_client):
        client    = Client()
        category  = Category.objects.get(id=1)
        amenity1  = Amenity.objects.get(id=1)
        amenity2  = Amenity.objects.get(id=2)
        
        class GmapsMockedResponse:
            def json(self):
                return [{
                        "formatted_address" : "test_address",
                                 "geometry" : {
                                 "location" : {
                                      "lat" : 37.4224764,
                                      "lng" : -122.0842499
                        }
                    }
                }]

        
        host_data = {
                    "id"          : 1,
                    "name"        : "room",
                    "min_date"    : "test_date",
                    "city"        : "test_type",
                    "category"    : "test_type",
                    "adult"       : "1",
                    "children"    : "3",
                    "is_refund"   : True,
                    "price"       : "40000",
                    "amenity"     : ["test_amenity", "test2_amenity"],
                    "address"     : "test_address"             
                }

        gmaps               = MagicMock()
        gmaps.geocode       = MagicMock(return_value= GmapsMockedResponse().json()) 
        geoclient_requests.return_value = gmaps
        user                = User.objects.get(id=1)
        room                = Room.objects.get(id=1)
        token               = jwt.encode({'id': user.id}, SECRET_KEY, algorithm = 'HS256')
        headers             = {"HTTP_Authorization": token}
        bucket              = "test"
        room_file_list      = self.generate_photo_file_list()
        file_urls_list      = [f"https://AWS_S3_CUSTOM_DOMAIN/room/{room_file}" for room_file in room_file_list]
        data                = {'room_file':room_file_list, 'room_info':''}
            
        for file_urls in file_urls_list:
            user.profile_url = file_urls
            user.save()
        response            = client.post("/user/host", data, **headers)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),
            {
                'message':"none room_info"
            }
        )

    @patch("user.views.boto3.client")
    @patch("user.views.googlemaps.Client")
    def test_host_registrate_none_file(self, geoclient_requests, mocked_client):
        client    = Client()
        category  = Category.objects.get(id=1)
        amenity1  = Amenity.objects.get(id=1)
        amenity2  = Amenity.objects.get(id=2)
        
        class GmapsMockedResponse:
            def json(self):
                return [{
                        "formatted_address" : "test_address",
                                 "geometry" : {
                                 "location" : {
                                      "lat" : 37.4224764,
                                      "lng" : -122.0842499
                        }
                    }
                }]

        
        host_data = {
                    "id"          : 1,
                    "name"        : "room",
                    "min_date"    : "test_date",
                    "city"        : "test_type",
                    "category"    : "test_type",
                    "adult"       : "1",
                    "children"    : "3",
                    "is_refund"   : True,
                    "price"       : "40000",
                    "amenity"     : ["test_amenity", "test2_amenity"],
                    "address"     : "test_address"             
                }

        gmaps               = MagicMock()
        gmaps.geocode       = MagicMock(return_value= GmapsMockedResponse().json()) 
        geoclient_requests.return_value = gmaps
        user                = User.objects.get(id=1)
        room                = Room.objects.get(id=1)
        token               = jwt.encode({'id': user.id}, SECRET_KEY, algorithm = 'HS256')
        headers             = {"HTTP_Authorization": token}
        bucket              = "test"
        room_file_list      = self.generate_photo_file_list()
        file_urls_list      = [f"https://AWS_S3_CUSTOM_DOMAIN/room/{room_file}" for room_file in room_file_list]
        data                = {'room_file':'', 'room_info':json.dumps(host_data)}
            
        for file_urls in file_urls_list:
            user.profile_url = file_urls
            user.save()
        response            = client.post("/user/host", data, **headers)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),
            {
                'message':"none file"
            }
        )

    @patch("user.views.boto3.client")
    @patch("user.views.googlemaps.Client")
    def test_host_registrate_none_send_address(self, geoclient_requests, mocked_client):
        client    = Client()
        category  = Category.objects.get(id=1)
        amenity1  = Amenity.objects.get(id=1)
        amenity2  = Amenity.objects.get(id=2)
        
        class GmapsMockedResponse:
            def json(self):
                return [{
                        "formatted_address" : "test_address",
                                 "geometry" : {
                                 "location" : {
                                      "lat" : 37.4224764,
                                      "lng" : -122.0842499
                        }
                    }
                }]

        
        host_data = {
                    "id"          : 1,
                    "name"        : "room",
                    "min_date"    : "test_date",
                    "city"        : "test_type",
                    "category"    : "test_type",
                    "adult"       : "1",
                    "children"    : "3",
                    "is_refund"   : True,
                    "price"       : "40000",
                    "amenity"     : ["test_amenity", "test2_amenity"],
                    "address"     : ""             
                }

        gmaps               = MagicMock()
        gmaps.geocode       = MagicMock(return_value= GmapsMockedResponse().json()) 
        geoclient_requests.return_value = gmaps
        user                = User.objects.get(id=1)
        room                = Room.objects.get(id=1)
        token               = jwt.encode({'id': user.id}, SECRET_KEY, algorithm = 'HS256')
        headers             = {"HTTP_Authorization": token}
        bucket              = "test"
        room_file_list      = self.generate_photo_file_list()
        file_urls_list      = [f"https://AWS_S3_CUSTOM_DOMAIN/room/{room_file}" for room_file in room_file_list]
        data                = {'room_file':room_file_list, 'room_info':json.dumps(host_data)}
            
        for file_urls in file_urls_list:
            user.profile_url = file_urls
            user.save()
        response            = client.post("/user/host", data, **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'none send ADDRESS'
            }
        )
    
    @patch("user.views.boto3.client")
    @patch("user.views.googlemaps.Client")
    def test_host_registrate_max_capacity(self, geoclient_requests, mocked_client):
        client    = Client()
        category  = Category.objects.get(id=1)
        amenity1  = Amenity.objects.get(id=1)
        amenity2  = Amenity.objects.get(id=2)
        
        class GmapsMockedResponse:
            def json(self):
                return [{
                        "formatted_address" : "test_address",
                                 "geometry" : {
                                 "location" : {
                                      "lat" : 37.4224764,
                                      "lng" : -122.0842499
                        }
                    }
                }]

        
        host_data = {
                    "id"          : 1,
                    "name"        : "room",
                    "min_date"    : "test_date",
                    "city"        : "test_type",
                    "category"    : "test_type",
                    "adult"       : "3",
                    "children"    : "3",
                    "is_refund"   : True,
                    "price"       : "40000",
                    "amenity"     : ["test_amenity", "test2_amenity"],
                    "address"     : "test_address"             
                }

        gmaps               = MagicMock()
        gmaps.geocode       = MagicMock(return_value= GmapsMockedResponse().json()) 
        geoclient_requests.return_value = gmaps
        user                = User.objects.get(id=1)
        room                = Room.objects.get(id=1)
        token               = jwt.encode({'id': user.id}, SECRET_KEY, algorithm = 'HS256')
        headers             = {"HTTP_Authorization": token}
        bucket              = "test"
        room_file_list      = self.generate_photo_file_list()
        file_urls_list      = [f"https://AWS_S3_CUSTOM_DOMAIN/room/{room_file}" for room_file in room_file_list]
        data                = {'room_file':room_file_list, 'room_info':json.dumps(host_data)}
            
        for file_urls in file_urls_list:
            user.profile_url = file_urls
            user.save()
        response            = client.post("/user/host", data, **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'max capacity'
            }
        )

    @patch("user.views.boto3.client")
    @patch("user.views.googlemaps.Client")
    def test_host_registrate_nonexistent_category(self, geoclient_requests, mocked_client):
        client    = Client()
        category  = Category.objects.get(id=1)
        amenity1  = Amenity.objects.get(id=1)
        amenity2  = Amenity.objects.get(id=2)
        
        class GmapsMockedResponse:
            def json(self):
                return [{
                        "formatted_address" : "test_address",
                                 "geometry" : {
                                 "location" : {
                                      "lat" : 37.4224764,
                                      "lng" : -122.0842499
                        }
                    }
                }]

        
        host_data = {
                    "id"          : 1,
                    "name"        : "room",
                    "min_date"    : "test_date",
                    "city"        : "test_type",
                    "category"    : "none_category",
                    "adult"       : "1",
                    "children"    : "3",
                    "is_refund"   : True,
                    "price"       : "40000",
                    "amenity"     : ["test_amenity", "test2_amenity"],
                    "address"     : "test_address"             
                }

        gmaps               = MagicMock()
        gmaps.geocode       = MagicMock(return_value= GmapsMockedResponse().json()) 
        geoclient_requests.return_value = gmaps
        user                = User.objects.get(id=1)
        room                = Room.objects.get(id=1)
        token               = jwt.encode({'id': user.id}, SECRET_KEY, algorithm = 'HS256')
        headers             = {"HTTP_Authorization": token}
        bucket              = "test"
        room_file_list      = self.generate_photo_file_list()
        file_urls_list      = [f"https://AWS_S3_CUSTOM_DOMAIN/room/{room_file}" for room_file in room_file_list]
        data                = {'room_file':room_file_list, 'room_info':json.dumps(host_data)}
            
        for file_urls in file_urls_list:
            user.profile_url = file_urls
            user.save()
        response            = client.post("/user/host", data, **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'nonexistent category'
            }
        )

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
        headers             = {'HTTP_Authorization':'test_token'}
        response            = client.get("/user/kakao", **headers)
        user_id             = MockedResponse().json()['id']
        access_token        = jwt.encode({'id':3}, SECRET_KEY, algorithm='HS256')

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
        image = PIL.new('RGBA', size=(100, 100), color=(155, 0, 0))
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
        response = client.post('/user/profile', data, **headers)
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
        response = client.post('/user/profile', data)
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
        response = client.post('/user/profile', data, **headers)
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
        response = client.post('/user/profile', data, **headers)
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
        response = client.post('/user/profile', data, **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'MESSAGE': 'KEY_ERROR'
            }
        )
        
class AuthEmailTest(TestCase):
    def setup(self):
        User.objects.create(
            id           = 1,
            email        = 'abc@gmail.com',
            password     = '123456789',
            first_name   = 'test_user_first_name',
            last_name    = 'test_user_last_name',
            sex          = 'M',
            birthday     = '0000-00-00',
            phone_number = 1012345678
        )
    
    def tearDown(self):
        User.objects.all().create()

    def test_send_success_email(self):
        client = Client()

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