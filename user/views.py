import json, bcrypt, jwt, requests
import boto3

from django.http      import JsonResponse
from django.views     import View
from django.shortcuts import redirect

from beerbnb.settings import SECRET_KEY, EMAIL
from user.models      import User
from user.validate    import validate_email, validate_password, validate_phone_number
from user.auth_email  import make_email_token, check_email_token, message
from my_settings      import MY_AWS_ACCESS_KEY_ID, MY_AWS_SECRET_ACCESS_KEY
from beerbnb.settings import AWS_S3_CUSTOM_DOMAIN

from django.utils.http              import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding          import force_bytes, force_text
from django.core.mail               import EmailMessage

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

            user = User.objects.create(
                first_name   = first_name,
                last_name    = last_name,
                email        = email,
                birthday     = birthday,
                sex          = sex,
                phone_number = phone_number,
                is_allowed   = False,
                password     = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            )

            domain       = EMAIL['REDIRECT_PAGE']
            uid64        = urlsafe_base64_encode(force_bytes(user.id))
            email_token  = make_email_token(user.id)
            message_data = message(domain, uid64, email_token)

            email = EmailMessage('Hi', message_data, to=[data['email']])
            email.send()

            return JsonResponse({'message':'SUCCESS'}, status=200)
<<<<<<< HEAD
=======
            
>>>>>>> 93f50b8... commit
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

            if not user.is_allowed:
                return JsonResponse({'message': 'UNAUTHORIZED_USER'}, status=401)
            
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
        
class ProfileUpload(View):
    def __init__(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id     = MY_AWS_ACCESS_KEY_ID,
            aws_secret_access_key = MY_AWS_SECRET_ACCESS_KEY  
            )
            
        self.bucket = 'beerbnb'

    def post(self, request): 
        file = request.FILES.get('file')

        if file:
            self.client.upload_fileobj(
                file,
                self.bucket,
                f'profile/{file}',
                ExtraArgs={
                    "ContentType": file.content_type
                }
            )

            file_urls = f"https://{AWS_S3_CUSTOM_DOMAIN}/profile/{file.name}" 
            
            return JsonResponse({'massage':'success'}, status=200)
        return JsonResponse({'massage':"none file"}, status=404)

class Auth(View):
    def get(self, request, uid64, email_token):
        uid  = force_text(urlsafe_base64_decode(uid64))
        user = User.objects.get(id=uid)

        if check_email_token(email_token):
            user.is_allowed = True
            user.save()

            return redirect(EMAIL['REDIRECT_PAGE'])
        
        return JsonResponse({'massage': 'auth fail'}, status = 400)
