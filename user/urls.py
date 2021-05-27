from django.urls import path

from user.views import Signin

urlpatterns = [
    path('/signin', Signin.as_view())
]