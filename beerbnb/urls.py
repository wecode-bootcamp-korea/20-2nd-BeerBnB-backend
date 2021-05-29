from django.urls  import path, include

urlpatterns = [
    path('rooms', include('room.urls')),
    path('user', include('user.urls')),
    path('reservation', include('reservation.urls'))
]
