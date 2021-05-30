import jwt, json

from django.http import JsonResponse

from my_settings import SECRET_KEY
from user.models import User

class LoginRequired:
    def __init__(self, fuc):
        self.fuc = fuc

    def __call__(self, request, *args, **kwargs):
        token = request.headers.get("Authorization", None)
        try:
            if access_token:    
                payload      = jwt.decode(access_token, SECRET_KEY, algorithms = 'HS256')
                user         = User.objects.get(id=payload['id'])
                request.user = user
                
                return self.fuc(self, request, *args, **kwargs)

            return JsonResponse({'MESSAGE' : 'NO LOGIN'}, status=401)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'MESSAGE': 'INVALID_TOKEN' }, status=400)

        except jwt.exceptions.InvalidSignatureError:
            return JsonResponse({'MESSAGE' : 'InvalidSignatureError'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status=401)