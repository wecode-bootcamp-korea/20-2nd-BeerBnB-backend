import json, bcrypt, jwt, requests, boto3, googlemaps
from uuid           import uuid4

from django.http      import JsonResponse
from django.views     import View
from django.shortcuts import redirect
from django.db        import transaction

from beerbnb.settings import SECRET_KEY, EMAIL
from user.models      import User, Host
from user.validate    import validate_email, validate_password, validate_phone_number
from user.auth_email  import make_email_token, check_email_token, message
from my_settings      import MY_AWS_ACCESS_KEY_ID, MY_AWS_SECRET_ACCESS_KEY, MY_GOOGLE_ACCESS_KEY_ID, AWS_S3_CUSTOM_DOMAIN, AWS_STORAGE_BUCKET_NAME
from beerbnb.settings import AWS_S3_CUSTOM_DOMAIN
from user.utils       import LoginRequired
from user.profile_utils import S3Client
from room.models      import Room, Amenity, DisableDate, AbleTime, Category, RoomAmenity, Image

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
            file_urls = s3_client.upload(file, file_name)

            user.profile_url = file_urls
            user.save()

            return JsonResponse({'massege':'create'}, status=200)
            
        except KeyError:
            return JsonResponse({"message" : "key error"}, status=400)

class Auth(View):
    def get(self, request, uid64, email_token):
        uid  = force_text(urlsafe_base64_decode(uid64))
        user = User.objects.get(id=uid)

        if check_email_token(email_token):
            user.is_allowed = True
            user.save()

            return redirect(EMAIL['REDIRECT_PAGE'])
        
        return JsonResponse({'massage': 'auth fail'}, status = 400)


class HostView(View):
    @LoginRequired
    @transaction.atomic
    def post(self, request):
        try:
            host, created = Host.objects.get_or_create(user=request.user)

            data = json.loads(request.body)

            name         = data['name']
            min_date     = data['min_date']
            city         = data['city']
            capacity     = data['capacity']
            is_refund    = data['is_refund']
            price        = data['price']
            category     = data['category']
            # checkin      = data['able_time'][0]
            # checkout     = data['able_time'][1]
            # start_date   = data['disable_date'][0]
            # end_date     = data['disable_date'][1]
            amenity_list = data['amenity']           
            address      = data['address']

            gmaps = googlemaps.Client(key=MY_GOOGLE_ACCESS_KEY_ID)

            geocode_result = gmaps.geocode(address,language='ko')
            
            if not geocode_result:
                return JsonResponse({'message':'INVALID ADDRESS'}, status=400)
            
            latitude     = geocode_result[0]['geometry']['location']['lat']
            longtitude   = geocode_result[0]['geometry']['location']['lng']

            disable_date = DisableDate.objects.create(
                start_date = start_date,
                end_date   = end_date   
            )

            able_time = AbleTime.objects.create(
                checkin  = checkin,
                checkout = checkout,
            )

            #filter로 수정(고정된 데이터 값)
            if not Category.objects.filter(name=category).exists():
                return JsonResponse({'message':'nonexistent category'}, status=400)

            category     = Category.objects.get(name=category)
            amenity_list = [Amenity.objects.create(name=amenity[0], image=amenity[1]) for amenity in amenity_list]
            
            room = Room.objects.create(
                name         = name,
                min_date     = min_date,
                city         = city,
                capacity     = capacity,
                latitude     = latitude,
                longtitude   = longtitude,
                is_refund    = is_refund,
                price        = price,
                host         = host,
                able_time    = able_time,
                disable_date = disable_date,
                category     = category
            )

            for amenity in amenity_list:
                RoomAmenity(room=room, amenity=amenity).save()

            return JsonResponse({'message':'success', 'room_id':room.id}, status=201)
        
        except KeyError:
            return JsonResponse({'message':'key error'}, status=404)



class HostUpload(View):
    @LoginRequired
    @transaction.atomic
    def post(self, request):
        try:
            client   = boto3.client(
            's3',
            aws_access_key_id     = MY_AWS_ACCESS_KEY_ID,
            aws_secret_access_key = MY_AWS_SECRET_ACCESS_KEY  
            )
            files    = request.FILES.getlist('room_file')
            room_id  = request.POST.get('room_id')
            user     = request.user
            if not user.is_allowed:
                return JsonResponse({'message':'none_host'}, status=404) 
                
            if not files:
                return JsonResponse({'message':"none file"}, status=404)
            
            if not Room.objects.filter(id=room_id).exists():
                return JsonResponse({'message':'none exist room'}, status =400)


            room = Room.objects.get(id=room_id)

            for file in files:
                client.upload_fileobj(
                        file,
                        AWS_STORAGE_BUCKET_NAME,
                        f'room/{file}',
                        ExtraArgs={
                            "ContentType": file.content_type
                        }
                    )
                file_urls = f"https://{AWS_S3_CUSTOM_DOMAIN}/profile/{file.name}" 
            
                Image.objects.create(url=file_urls, room=room)

            return JsonResponse({'message':'success'}, status=200)
            
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
            file_urls = s3_client.upload(file, file_name)

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
