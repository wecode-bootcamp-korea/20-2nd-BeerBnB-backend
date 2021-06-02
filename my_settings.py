DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'beerbnb',
        'USER': 'root',
        'PASSWORD': '123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

SECRET_KEY = 'django-insecure-@cnjp%qyzj^*3d9u10#e*!)!g7&8iij!k@&g__68f1f-+55$5$'

REST_API_KEY = "dc80d2f79d67392436ce1852ad0103fe"

MY_GOOGLE_ACCESS_KEY_ID = "AIzaSyBiIjBAQKo2ibq1bZyH0y7b5WRuP_GcBhk"

MY_AWS_ACCESS_KEY_ID = "AKIA3JW53HCHFHF6T73R"
MY_AWS_SECRET_ACCESS_KEY = "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"

MY_NAVER_ACCESS_KEY_ID = "IKoXP8PnBWjsh8YMuj9c"
MY_NAVER_SECRET_KEY = "WlIF4S8OTHygGC8zkA4ESpwQjgsAjOKEX59TAk42"
MY_PHONE_NUMBER = "01055396705"
MY_SERVICE_ID = "ncp:sms:kr:267859014089:test-project"

AWS_REGION = "ap-northeast-2"
AWS_STORAGE_BUCKET_NAME = "beerbnb"
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME,AWS_REGION)

EMAIL = {
    'EMAIL_BACKEND'      : 'django.core.mail.backends.smtp.EmailBackend',
    'EMAIL_USE_TLS'      : True,
    'EMAIL_PORT'         : 587,
    'EMAIL_HOST'         : 'smtp.gmail.com',
    'EMAIL_HOST_USER'    : 'dnstks0204@gmail.com',
    'EMAIL_HOST_PASSWORD': '@dns026469',
    'SERVER_EMAIL'       : 'dnstks0204@gmail.com',
    'REDIRECT_PAGE'      : 'http://localhost:5000'
}