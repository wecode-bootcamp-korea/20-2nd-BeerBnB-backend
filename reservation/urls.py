from django.urls   import path

from reservation.views import ReservationView

urlpatterns = [
    path('', ReservationView.as_view()),
]