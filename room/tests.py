from django.test      import TestCase, Client

from room.models      import Room, Category, RoomAmenity, Image, Amenity, WishList, DisableDate, AbleTime
from user.models      import User,Host, Review

class RoomDetailTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category=Category.objects.create(
                id   = 1,
                name = '아파트'
            )
        user=User.objects.create(
            id         = 1,
            first_name = '하나',
            last_name  = '김',
        )
        host=Host.objects.create(
            id       = 1,
            user     = user,
            is_super = True
        )
        disabledate=DisableDate.objects.create(
            id         = 1,
            start_date = '2021-06-03',
            end_date   = '2021-07-09'
        )
        abletime=AbleTime.objects.create(
            id       = 1,
            checkin  = '11:00:00',
            checkout = '13:00:00'
        )
        room=Room.objects.create(
            id           = 1,
            name         = '양재아파트',
            city         = '서울 양재동',
            price        = 100000,
            category     = category,
            host         = host,
            latitude     = 1.0221111,
            longtitude   = 2.2222211,
            capacity     = 3,
            disable_date = disabledate,
            able_time    = abletime
        )
        Image.objects.create(
            id   = 1,
            room = room,
            url  = 'a'
        )
        
        amenity1=Amenity.objects.create(
            id    = 1,
            name  = '와인',
            image = '<i class="fas fa-fan"></i>'
        )

        amenity2=Amenity.objects.create(
            id    = 2,
            name  = '맥주',
            image = '<i class="fas fa-beer"></i>'
        )

        RoomAmenity.objects.create(
            id      = 1,
            room    = room,
            amenity = amenity1
        )

        RoomAmenity.objects.create(
            id      = 2,
            room    = room,
            amenity = amenity2
        )
        Review.objects.create(
            id                = 1,
            review_user       = user,
            review_room       = room,
            cleanliness       = 3.0,
            communication     = 2.0,
            checkin           = 4.0,
            accuracy          = 4.0,
            location          = 2.0,
            cost_effectivenes = 4.0
        )

    def test_roomdetail_get_view(self):
        client   = Client()
        response = client.get('/rooms/1')
        self.assertEqual(response.json(), {
            'detail': 
                {
                    'room_name': '양재아파트',
                    'address'  : '서울 양재동',
                    'price'    : '100000.00',
                    'room_type': '아파트',
                    'image'    : 'a',
                    'is_super' : True,
                    'host'     : '김하나',
                    'capacity' : 3,
                    'amenity'  : [
                            {
                            'id'         : 1,
                            'icon'       : 'fas fa-fan',
                            'description': '와인'
                            },
                            {
                            'id'         : 2,
                            'icon'       : 'fas fa-beer',
                            'description': '맥주'
                            }
                        ],
                    'rating' : [
                        {
                        'category'       : 'cleanliness',
                        'category_rating': 3.0
                    },
                    {
                        'category'       : 'communication',
                        'category_rating': 2.0
                    },
                    {
                        'category'       : 'checkin',
                        'category_rating': 4.0
                    },
                    {
                        'category'       : 'accuracy',
                        'category_rating': 4.0
                    },
                    {
                        'category'       : 'location',
                        'category_rating': 2.0
                    },
                    {
                        'category'       : 'cost_effectivenes',
                        'category_rating': 4.0
                    }
                    ]
                }
        })
        self.assertEqual(response.status_code, 200)
        
    def test_roomdetail_invalid_room_view(self):
        client   = Client()
        response = client.get('/rooms/999')
        self.assertEqual(response.json(),{'message':'NOT_FOUND_ROOM_ID'})
        self.assertEqual(response.status_code, 400)