<<<<<<< HEAD
from django.urls import path

<<<<<<< HEAD
=======
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> e6d6d76... commit
=======
<<<<<<< HEAD
>>>>>>> d5fa9d3... social login
from user.views import Signup, Signin, KaKaoSignIn
=======
from user.views import Signup, Signin
>>>>>>> 4d825b5... commit

urlpatterns = [
    path('/signup', Signup.as_view()),
    path('/signin', Signin.as_view()),
    path('/kakao', KaKaoSignIn.as_view())
<<<<<<< HEAD
=======
=======
from user.views import Signin

urlpatterns = [
    path('/signin', Signin.as_view())
>>>>>>> 7dc3f5a... commit
=======
from user.views import KaKaoSignIn

urlpatterns = [
    path('/kakao', KaKaoSignIn.as_view())
>>>>>>> cd6ce12... social login
<<<<<<< HEAD
>>>>>>> d5fa9d3... social login
=======
=======
from django.urls   import path

from user.views import ProfileUpload

urlpatterns = [
    path('/upload', ProfileUpload.as_view()),
>>>>>>> b2b15cb... upload
>>>>>>> 1cb79c1... upload
]