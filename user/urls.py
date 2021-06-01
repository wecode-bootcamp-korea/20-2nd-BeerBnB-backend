<<<<<<< HEAD
<<<<<<< HEAD
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
<<<<<<< HEAD
>>>>>>> d5fa9d3... social login
=======
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> d59e24d... commit
=======
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 58262ea... upload
=======
<<<<<<< HEAD
>>>>>>> 15f54a4... commit
from user.views import Signup, Signin, KaKaoSignIn
=======
from user.views import Signup, Signin
>>>>>>> 4d825b5... commit
=======
from user.views import Signup, Signin, KaKaoSignIn, ProfileUpload, Auth
>>>>>>> ee691ea... commit
=======
from user.views import Signup, Signin, KaKaoSignIn, ProfileUpload
>>>>>>> f5972cb... upload
=======
from user.views import Signup, Signin, KaKaoSignIn, ProfileUpload, Auth
>>>>>>> 0b6272a... commit

urlpatterns = [
    path('/signup', Signup.as_view()),
    path('/signin', Signin.as_view()),
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    path('/kakao', KaKaoSignIn.as_view())
<<<<<<< HEAD
=======
=======
from user.views import Signin

urlpatterns = [
    path('/signin', Signin.as_view())
>>>>>>> 7dc3f5a... commit
=======
=======
from django.urls import path

>>>>>>> a94e80e... social login
from user.views import KaKaoSignIn

urlpatterns = [
    path('/kakao', KaKaoSignIn.as_view())
<<<<<<< HEAD
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
<<<<<<< HEAD
>>>>>>> 1cb79c1... upload
=======
=======
from django.urls import path
from user.views  import Signup, Auth

urlpatterns = [
    path('/signup', Signup.as_view()),
    path('/auth/<str:uidb64>/<str:email_token>', Auth.as_view())
>>>>>>> 666ebdc... auth_email
<<<<<<< HEAD
>>>>>>> b091a65... auth_email
=======
=======
>>>>>>> a94e80e... social login
<<<<<<< HEAD
>>>>>>> 65f2a33... dev
=======
=======
    path('/kakao', KaKaoSignIn.as_view()),
    path('/upload', ProfileUpload.as_view()),
    path('/auth/<str:uidb64>/<str:email_token>', Auth.as_view())
>>>>>>> ee691ea... commit
<<<<<<< HEAD
>>>>>>> d59e24d... commit
=======
=======
    path('/kakao', KaKaoSignIn.as_view()),
    path('/upload', ProfileUpload.as_view())
>>>>>>> f5972cb... upload
<<<<<<< HEAD
>>>>>>> 58262ea... upload
=======
=======
    path('/kakao', KaKaoSignIn.as_view()),
    path('/upload', ProfileUpload.as_view()),
    path('/auth/<str:uidb64>/<str:email_token>', Auth.as_view())
>>>>>>> 0b6272a... commit
>>>>>>> 15f54a4... commit
]