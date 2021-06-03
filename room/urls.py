from django.urls    import path
from .views         import WishListView, RoomView,RoomListView

urlpatterns = [
    path('/<int:room_id>', RoomView.as_view()),
    path('/wishlist', WishListView.as_view()),
    path('/wishlist/<int:room_id>', WishListView.as_view()),
    path('', RoomListView.as_view())
]