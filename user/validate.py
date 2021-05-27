import re

from user.models import User

RANGE_PASSWORD= '{8,}'

def validate_email(email):
    regex = re.compile('^[a-z0-9+-_.]+@[a-z0-9-]+\.[a-z0-9-.]+$', re.I)
    match = regex.match(str(email))
    return bool(match)

def validate_password(password):
    regex = re.compile('^[a-z0-9_-]'+ RANGE_PASSWORD +'$', re.I)
    match = regex.match(str(password))
    return bool(match)

def validate_phone_number(phone_number):
    regex = re.compile('^[0-9]{2}([0-9]{3}|[0-9]{4})[0-9]{4}$', re.I)
    match = regex.match(str(phone_number))
    return bool(match)