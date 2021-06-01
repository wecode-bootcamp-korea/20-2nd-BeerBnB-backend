from django.urls import path

from user.views import Signup, Signin, KaKaoSignIn, ProfileUpload, Auth

urlpatterns = [
    path('/signup', Signup.as_view()),
    path('/signin', Signin.as_view()),
    path('/kakao', KaKaoSignIn.as_view()),
    path('/upload', ProfileUpload.as_view()),
    path('/auth/<str:uidb64>/<str:email_token>', Auth.as_view())
]