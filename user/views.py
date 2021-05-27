import json, bcrypt, jwt

from django.http    import JsonResponse
from django.views   import View

from beerbnb.settings import SECRET_KEY
from user.models      import User

class Signin(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            email    = data['email']
            password = data['password'].encode('utf-8')

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)

            user            = User.objects.get(email=email)
            user_password   = user.password.encode('utf-8')

            if not bcrypt.checkpw(password, user_password):
                return JsonResponse({'MASSAGE': 'INVALID_USER'}, status=401)

            data         = {'user_id':user.id}
            access_token = jwt.encode(data, SECRET_KEY, algorithm='HS256')   
            return JsonResponse({'MESSAGE':'SUCCESS' , 'token':access_token}, status=200)

        except KeyError:
            return JsonResponse({'MASSAGE':'KEYERROR'}, status=400)