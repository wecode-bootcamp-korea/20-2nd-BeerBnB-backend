from django.urls    import path
from .views         import RoomView,RoomListView

urlpatterns = [
    path('/<int:room_id>', RoomView.as_view()),
    path('', RoomListView.as_view())
]