from django.urls import path

from user.views import Signup, Signin, KaKaoSignIn

urlpatterns = [
    path('/signup', Signup.as_view()),
    path('/signin', Signin.as_view()),
    path('/kakao', KaKaoSignIn.as_view())
]