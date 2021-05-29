from django.urls import path

from user.views import Signup, Signin, KaKaoSignIn, HostView, HostUpload

urlpatterns = [
    path('/signup', Signup.as_view()),
    path('/signin', Signin.as_view()),
    path('/kakao', KaKaoSignIn.as_view()),
    path('/host', HostView.as_view()),
    path('/upload', HostUpload.as_view())
]