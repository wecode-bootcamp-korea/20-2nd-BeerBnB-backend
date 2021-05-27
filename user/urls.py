from django.urls import path

from user.views import Signup

urlpatterns = [
    path('/signup', Signup.as_view()),
    path('/signin', Signin.as_view())
]