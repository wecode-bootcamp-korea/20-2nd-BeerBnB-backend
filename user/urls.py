from django.urls import path

from user.views import Signup, Signin, KaKaoSignIn, ProfileUpload, ProfileUploadUpdate, ProfileDelete

urlpatterns = [
    path('/signup', Signup.as_view()),
    path('/signin', Signin.as_view()),
    path('/kakao', KaKaoSignIn.as_view()),
    path('/upload', ProfileUpload.as_view()),
    path('/update', ProfileUploadUpdate.as_view()),
    path('/delete', ProfileDelete.as_view())
]