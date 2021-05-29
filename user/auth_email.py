import jwt
from django.core.exceptions import ObjectDoesNotExist

from user.models      import User
from beerbnb.settings import SECRET_KEY

def make_email_token(user_id):
    email_token = jwt.encode({'id':user_id}, SECRET_KEY, algorithm='HS256')
    return email_token

def check_email_token(email_token):
    try:
        payload = jwt.decode(email_token, SECRET_KEY, algorithms='HS256')
        user    = User.objects.get(id=payload['id'])   
        return True

    except jwt.exceptions.DecodeError:
        return False

    except User.DoesNotExist:
        return False

def message(domain, uid64, email_token):
    massage = f'Click on the link to complete your membership. \n Link : http://{domain}/user/auth/{uid64}/{email_token}'
    return massage