from django.urls import path

from user.views import Signup, Signin, KaKaoSignIn, ProfileUpload, ProfileUploadUpdate, ProfileDelete, Auth

urlpatterns = [
    path('/signup', Signup.as_view()),
    path('/signin', Signin.as_view()),
    path('/kakao', KaKaoSignIn.as_view()),
    path('/profile', ProfileUpload.as_view()),
    path('/profile', ProfileUploadUpdate.as_view()),
    path('/profile', ProfileDelete.as_view()),
    path('/auth/<str:uid64>/<str:email_token>', Auth.as_view())
]