import json, bcrypt, jwt, requests
import boto3
from uuid           import uuid4

from django.http    import JsonResponse
from django.views   import View

from user.models      import User
from user.validate    import validate_email, validate_password, validate_phone_number
from user.utils       import LoginRequired
from my_settings      import MY_AWS_ACCESS_KEY_ID, MY_AWS_SECRET_ACCESS_KEY, AWS_S3_CUSTOM_DOMAIN, AWS_STORAGE_BUCKET_NAME
from beerbnb.settings import SECRET_KEY
from user.file_utils  import S3Client

class Signup(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            email        = data['email']
            password     = data['password']
            first_name   = data['first_name']
            last_name    = data['last_name']
            sex          = data['sex']
            birthday     = data['birthday']
            phone_number = data['phone_number']

            if not validate_email(email):
                return JsonResponse({'message':'INVALID EMAIL'}, status=400)

            if not validate_password(password):
                return JsonResponse({'message':'INVALID PASSWORD'}, status=400)

            if not validate_phone_number(phone_number):
                return JsonResponse({'message':'INVALID PHONE NUMBER'}, status=400)

            if User.objects.filter(first_name = first_name, last_name = last_name).exists():
                return JsonResponse({'message':'DUPLICATE NAME'}, status=400)

            if User.objects.filter(email = email).exists():
                return JsonResponse({'message':'DUPLICATE EMAIL'}, status=400)

            if User.objects.filter(phone_number = phone_number).exists():
                return JsonResponse({'message':'DUPLICATE PHONE_NUMBER'}, status=400)

            User.objects.create(
                first_name   = first_name,
                last_name    = last_name,
                email        = email,
                birthday     = birthday,
                phone_number = phone_number,
                password     = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            )
            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=400)

class Signin(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            email    = data['email']
            password = data['password'].encode('utf-8')

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'INVALID_USER'}, status=401)

            user            = User.objects.get(email=email)
            user_password   = user.password.encode('utf-8')

            # if not user.is_allowed:
            #     return JsonResponse({'message': 'UNAUTHORIZED_USER'}, status=401)
            
            if not bcrypt.checkpw(password, user_password):
                return JsonResponse({'message': 'INVALID_USER'}, status=401)

            data         = {'id':user.id}
            access_token = jwt.encode(data, SECRET_KEY, algorithm='HS256')   
            return JsonResponse({'message':'SUCCESS' , 'token':access_token}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEYERROR'}, status=400)
            
class KaKaoSignIn(View):
    def get(self, request):
        try:
            kakao_token = request.headers.get("Authorization", None)
            api_url     = "https://kapi.kakao.com/v2/user/me"
            token_type  = "Bearer"

            if not kakao_token:
                return JsonResponse({'message': "TOKEN REQUIRED"}, status=400)

            response = requests.get(
                api_url, 
                headers= {
                    'Authorization':f'{token_type} {kakao_token}'
                }
            ).json()
            error_massage = response.get('msg', None)

            if error_massage:
                return JsonResponse({'massege' : error_massage}, status = 400)

            kakao_account = response.get("kakao_account", None)

            if 'email' not in kakao_account:
                return JsonResponse({'message':'EMAIL REQUIRED'}, status=405)

            user, created = User.objects.get_or_create(
                social_id = response.get('id'),
                email     = kakao_account.get('email'),
                sex       = kakao_account.get('gender'),
                birthday  = kakao_account.get('birthday')
            )

            access_token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm='HS256')
            if not created:
                return JsonResponse({'message':'created user' , 'access_token':access_token}, status=200)
            return JsonResponse({'message':'existing user' , 'access_token':access_token}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=404)

client = boto3.client(
            's3',
            aws_access_key_id     = MY_AWS_ACCESS_KEY_ID,
            aws_secret_access_key = MY_AWS_SECRET_ACCESS_KEY  
            )

class ProfileUpload(View):
    @LoginRequired
    def post(self, request): 
        try:
            file   = request.FILES.get('profile_file')
            user   = request.user
            if not file:
                return JsonResponse({'massage':"none file"}, status=404)
            
            s3_client = S3Client(client)
            file_name = uuid4().hex
            s3_client.upload(file, file_name)

            
            file_urls = f"https://{AWS_S3_CUSTOM_DOMAIN}/profile/{file_name}" 

            user.profile_url = file_urls
            user.save()

            return JsonResponse({'massege':'create'}, status=200)
            
        except KeyError:
            return JsonResponse({"message" : "key error"}, status=400)

class ProfileUploadUpdate(View):
    @LoginRequired
    def post(self, request): 
        try:
            file   = request.FILES.get('profile_file')
            user   = request.user
            if not file:
                return JsonResponse({'massage':"none file"}, status=404)
            
            if not user.profile_url:
                return JsonResponse({'message':'none profile'}, status=400)
            
            file_name = user.profile_url.replace(f"https://{AWS_S3_CUSTOM_DOMAIN}/", "")
            s3_client = S3Client(client)
            s3_client.delete(file_name)

            file_name = uuid4().hex
            s3_client.upload(file, file_name)

            file_urls = f"https://{AWS_S3_CUSTOM_DOMAIN}/profile/{file_name}" 
            user.profile_url = file_urls
            user.save()

            return JsonResponse({'massege':'update'}, status=200)
            
        except KeyError:
            return JsonResponse({"message" : "key error"}, status=400)

class ProfileDelete(View):
    @LoginRequired
    def post(self, request): 
        try:
            user   = request.user

            if not user.profile_url:
                return JsonResponse({'message':'none profile'}, status=400)

            file_name = user.profile_url.replace(f"https://{AWS_S3_CUSTOM_DOMAIN}/", "")
            user.profile_url = None
            user.save()

            s3_client = S3Client(client)
            s3_client.delete(file_name)

            return JsonResponse({'massege':'delete'}, status=200)
            
        except KeyError:
            return JsonResponse({"message" : "key error"}, status=400)