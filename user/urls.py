from django.urls import path

from user.views import Signup, Signin, KaKaoSignIn, ProfileUpload, ProfileUploadUpdate, ProfileDelete, Auth, HostView, SMSAuthView

urlpatterns = [
    path('/signup', Signup.as_view()),
    path('/signin', Signin.as_view()),
    path('/kakao', KaKaoSignIn.as_view()),
    path('/profile', ProfileUpload.as_view()),
    path('/host', HostView.as_view()),
    path('', SMSAuthView.as_view())
]