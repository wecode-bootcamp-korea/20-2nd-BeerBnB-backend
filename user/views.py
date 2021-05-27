import json, bcrypt, jwt

from django.http    import JsonResponse
from django.views   import View

from beerbnb.settings import SECRET_KEY
from user.models      import User
from user.validate    import validate_email, validate_password, validate_phone_number

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

            if not user.is_auth:
                return JsonResponse({'message': 'UNAUTHORIZED_USER'}, status=401)
            
            if not bcrypt.checkpw(password, user_password):
                return JsonResponse({'message': 'INVALID_USER'}, status=401)

            data         = {'user_id':user.id}
            access_token = jwt.encode(data, SECRET_KEY, algorithm='HS256')   
            return JsonResponse({'message':'SUCCESS' , 'token':access_token}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEYERROR'}, status=400)
