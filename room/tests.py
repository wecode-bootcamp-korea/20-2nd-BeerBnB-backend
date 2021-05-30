from django.test        import TestCase, Client

from room.models        import Room, Category, RoomAmenity, Image, Amenity, WishList, DisableDate, AbleTime
from user.models        import User,Host, Review
from reservation.models import Reservation, Status
from reservation.check  import check, check_in, check_out
from my_settings        import SECRET_KEY

class RoomTest(TestCase):
    @classmethod					
    def setUpTestData(cls):
        status=Status.objects.create(
            id = 1,
            status = 'reservation'
        )
        category=Category.objects.create(
                id   = 1,
                name = '아파트'
            )
        user1=User.objects.create(
            id         = 1,
            first_name = '하나',
            last_name  = '김',
        )
        user2=User.objects.create(
            id         = 2,
            first_name = '두리',
            last_name  = '김',
        )
        host1=Host.objects.create(
            id       = 1,
            user     = user1,
            is_super = True
        )
        host2=Host.objects.create(
            id       = 2,
            user     = user2,
            is_super = False
        )
        disabledate=DisableDate.objects.create(
            id         = 1,
            start_date = '2021-06-03',
            end_date   = '2021-07-09'
        )
        abledate=AbleTime.objects.create(
            id       = 1,
            checkin  = '11:00:00',
            checkout = '13:00:00'
        )
        room1=Room.objects.create(
            id           = 1,
            name         = '양재아파트',
            city         = '서울 양재동',
            price        = 100000,
            category     = category,
            host         = host1,
            is_refund    = True,
            latitude     = 1.0221111,
            longtitude   = 2.2222211,
            capacity     = 3,
            disable_date = disabledate,
            able_time    = abledate
        )
        room2=Room.objects.create(
            id           = 2,
            name         = '강남아파트',
            city         = '서울 강남',
            price        = 150000,
            category     = category,
            host         = host2,
            latitude     = 2.0221111,
            longtitude   = 3.2222211,
            capacity     = 4,
            disable_date = disabledate,
            able_time    = abledate
        )
        Image.objects.create(
            id   = 1,
            room = room1,
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
            room    = room1,
            amenity = amenity1
        )
        RoomAmenity.objects.create(
            id      = 2,
            room    = room1,
            amenity = amenity2
        )
        RoomAmenity.objects.create(
            id      = 3,
            room    = room2,
            amenity = amenity2
        )
        Review.objects.create(
            id                = 1,
            review_user       = user1,
            review_room       = room1,
            cleanliness       = 3.0,
            communication     = 2.0,
            checkin           = 4.0,
            accuracy          = 4.0,
            location          = 2.0,
            cost_effectivenes = 4.0
        )
        Review.objects.create(
            id                = 2,
            review_user       = user2,
            review_room       = room2,
            cleanliness       = 3.0,
            communication     = 2.0,
            checkin           = 4.0,
            accuracy          = 4.0,
            location          = 2.0,
            cost_effectivenes = 4.0
        )
        Reservation.objects.create(
            id       = 1,
            user     = user1,
            room     = room1,
            status   = status,
            checkin  = '2021-06-07',
            checkout = '2021-06-18'
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
        Status.objects.all().delete()

    def test_room_non_filter_thumbnail_view(self):
        client   = Client()
        response = client.get('/rooms')
        self.assertEqual(response.json(), {
            'thumbnail': [
                {
                    'room_id'  : Room.objects.get(id=1).id,
                    'room_name': '양재아파트',
                    'price'    : '100000.00',
                    'address'  : '서울 양재동',
                    'room_type': '아파트',
                    'lat'      : '1.0221111',
                    'lng'      : '2.2222211',
                    'image'    : ['a'],
                    'is_super' : True,
                    'capacity' : 3,
                    'amenity'  : ['와인','맥주'],
                    'rating' : [
                        {
                        'category'       : 'cleanliness',
                        'category_rating': '3.00000'
                    },
                    {
                        'category'       : 'communication',
                        'category_rating': '2.00000'
                    },
                    {
                        'category'       : 'checkin',
                        'category_rating': '4.00000'
                    },
                    {
                        'category'       : 'accuracy',
                        'category_rating': '4.00000'
                    },
                    {
                        'category'       : 'location',
                        'category_rating': '2.00000'
                    },
                    {
                        'category'       : 'cost_effectivenes',
                        'category_rating': '4.00000'
                    }
                    ]
                },
                {
                    'room_id'  : Room.objects.get(id=2).id,
                    'room_name': '강남아파트',
                    'price'    : '150000.00',
                    'address'  : '서울 강남',
                    'room_type': '아파트',
                    'lat'      : '2.0221111',
                    'lng'      : '3.2222211',
                    'image'    : [],
                    'is_super' : False,
                    'capacity' : 4,
                    'amenity'  : ['맥주'],
                    'rating' : [
                        {
                        'category'       : 'cleanliness',
                        'category_rating': '3.00000'
                    },
                    {
                        'category'       : 'communication',
                        'category_rating': '2.00000'
                    },
                    {
                        'category'       : 'checkin',
                        'category_rating': '4.00000'
                    },
                    {
                        'category'       : 'accuracy',
                        'category_rating': '4.00000'
                    },
                    {
                        'category'       : 'location',
                        'category_rating': '2.00000'
                    },
                    {
                        'category'       : 'cost_effectivenes',
                        'category_rating': '4.00000'
                    }
                    ]
                }],
            'common' : 2
            
        })
        self.assertEqual(response.status_code, 200)
    
    def test_room_city_filter_thumbnail_view(self):
        client   = Client()
        response = client.get('/rooms?city=양재')
        self.assertEqual(response.json(), {
            'thumbnail': [
                {
                    'room_id'  : Room.objects.get(id=1).id,
                    'room_name': '양재아파트',
                    'price'    : '100000.00',
                    'address'  : '서울 양재동',
                    'room_type': '아파트',
                    'lat'      : '1.0221111',
                    'lng'      : '2.2222211',
                    'image'    : ['a'],
                    'is_super' : True,
                    'capacity' : 3,
                    'amenity'  : ['와인','맥주'],
                    'rating' : [
                        {
                        'category'       : 'cleanliness',
                        'category_rating': '3.00000'
                    },
                    {
                        'category'       : 'communication',
                        'category_rating': '2.00000'
                    },
                    {
                        'category'       : 'checkin',
                        'category_rating': '4.00000'
                    },
                    {
                        'category'       : 'accuracy',
                        'category_rating': '4.00000'
                    },
                    {
                        'category'       : 'location',
                        'category_rating': '2.00000'
                    },
                    {
                        'category'       : 'cost_effectivenes',
                        'category_rating': '4.00000'
                    }
                    ]
                }
                    ]
                ,
            'common' : 1
            
        })
        self.assertEqual(response.status_code, 200)
    
    def test_room_price_filter_thumbnail_view(self):
        client   = Client()
        response = client.get('/rooms?min_price=90000&max_price=100000')
        self.assertEqual(response.json(), {
            'thumbnail': [
                {
                    'room_id'  : Room.objects.get(id=1).id,
                    'room_name': '양재아파트',
                    'price'    : '100000.00',
                    'address'  : '서울 양재동',
                    'room_type': '아파트',
                    'lat'      : '1.0221111',
                    'lng'      : '2.2222211',
                    'image'    : ['a'],
                    'is_super' : True,
                    'capacity' : 3,
                    'amenity'  : ['와인','맥주'],
                    'rating' : [
                        {
                        'category'       : 'cleanliness',
                        'category_rating': '3.00000'
                    },
                    {
                        'category'       : 'communication',
                        'category_rating': '2.00000'
                    },
                    {
                        'category'       : 'checkin',
                        'category_rating': '4.00000'
                    },
                    {
                        'category'       : 'accuracy',
                        'category_rating': '4.00000'
                    },
                    {
                        'category'       : 'location',
                        'category_rating': '2.00000'
                    },
                    {
                        'category'       : 'cost_effectivenes',
                        'category_rating': '4.00000'
                    }
                    ]
                }
                    ]
                ,
            'common' : 1
            
        })
        self.assertEqual(response.status_code, 200)

    def test_room_capacity_filter_thumbnail_view(self):
            client   = Client()
            response = client.get('/rooms?adult=1&child=3')
            self.assertEqual(response.json(), {
                'thumbnail': [
                    {
                        'room_id'  : Room.objects.get(id=2).id,
                        'room_name': '강남아파트',
                        'price'    : '150000.00',
                        'address'  : '서울 강남',
                        'room_type': '아파트',
                        'lat'      : '2.0221111',
                        'lng'      : '3.2222211',
                        'image'    : [],
                        'is_super' : False,
                        'capacity' : 4,
                        'amenity'  : ['맥주'],
                        'rating' : [
                            {
                            'category'       : 'cleanliness',
                            'category_rating': '3.00000'
                        },
                        {
                            'category'       : 'communication',
                            'category_rating': '2.00000'
                        },
                        {
                            'category'       : 'checkin',
                            'category_rating': '4.00000'
                        },
                        {
                            'category'       : 'accuracy',
                            'category_rating': '4.00000'
                        },
                        {
                            'category'       : 'location',
                            'category_rating': '2.00000'
                        },
                        {
                            'category'       : 'cost_effectivenes',
                            'category_rating': '4.00000'
                        }
                        ]
                    }
                        ]
                    ,
                'common' : 1
                
            })
            self.assertEqual(response.status_code, 200)

    def test_room_superhost_filter_thumbnail_view(self):
            client   = Client()
            response = client.get('/rooms?is_super=true')
            self.assertEqual(response.json(), {
                'thumbnail': [{
                    'room_id'  : Room.objects.get(id=1).id,
                    'room_name': '양재아파트',
                    'price'    : '100000.00',
                    'address'  : '서울 양재동',
                    'room_type': '아파트',
                    'lat'      : '1.0221111',
                    'lng'      : '2.2222211',
                    'image'    : ['a'],
                    'is_super' : True,
                    'capacity' : 3,
                    'amenity'  : ['와인','맥주'],
                    'rating' : [
                        {
                        'category'       : 'cleanliness',
                        'category_rating': '3.00000'
                    },
                    {
                        'category'       : 'communication',
                        'category_rating': '2.00000'
                    },
                    {
                        'category'       : 'checkin',
                        'category_rating': '4.00000'
                    },
                    {
                        'category'       : 'accuracy',
                        'category_rating': '4.00000'
                    },
                    {
                        'category'       : 'location',
                        'category_rating': '2.00000'
                    },
                    {
                        'category'       : 'cost_effectivenes',
                        'category_rating': '4.00000'
                    }
                    ]
                }],'common' : 1})
            self.assertEqual(response.status_code, 200)

    def test_room_refund_filter_thumbnail_view(self):
            client   = Client()
            response = client.get('/rooms?is_refund=true')
            self.assertEqual(response.json(), {
                'thumbnail': [{
                    'room_id'  : Room.objects.get(id=1).id,
                    'room_name': '양재아파트',
                    'price'    : '100000.00',
                    'address'  : '서울 양재동',
                    'room_type': '아파트',
                    'lat'      : '1.0221111',
                    'lng'      : '2.2222211',
                    'image'    : ['a'],
                    'is_super' : True,
                    'capacity' : 3,
                    'amenity'  : ['와인','맥주'],
                    'rating' : [
                        {
                        'category'       : 'cleanliness',
                        'category_rating': '3.00000'
                    },
                    {
                        'category'       : 'communication',
                        'category_rating': '2.00000'
                    },
                    {
                        'category'       : 'checkin',
                        'category_rating': '4.00000'
                    },
                    {
                        'category'       : 'accuracy',
                        'category_rating': '4.00000'
                    },
                    {
                        'category'       : 'location',
                        'category_rating': '2.00000'
                    },
                    {
                        'category'       : 'cost_effectivenes',
                        'category_rating': '4.00000'
                    }
                    ]
                }],'common' : 1})
            self.assertEqual(response.status_code, 200)

    def test_room_date_filter_thumbnail_view(self):
            client   = Client()
            response = client.get('/rooms?checkin=2021-06-14')
            self.assertEqual(response.json(), {
                'thumbnail':[{
                        'room_id'  : Room.objects.get(id=2).id,
                        'room_name': '강남아파트',
                        'price'    : '150000.00',
                        'address'  : '서울 강남',
                        'room_type': '아파트',
                        'lat'      : '2.0221111',
                        'lng'      : '3.2222211',
                        'image'    : [],
                        'is_super' : False,
                        'capacity' : 4,
                        'amenity'  : ['맥주'],
                        'rating' : [
                            {
                            'category'       : 'cleanliness',
                            'category_rating': '3.00000'
                        },
                        {
                            'category'       : 'communication',
                            'category_rating': '2.00000'
                        },
                        {
                            'category'       : 'checkin',
                            'category_rating': '4.00000'
                        },
                        {
                            'category'       : 'accuracy',
                            'category_rating': '4.00000'
                        },
                        {
                            'category'       : 'location',
                            'category_rating': '2.00000'
                        },
                        {
                            'category'       : 'cost_effectivenes',
                            'category_rating': '4.00000'
                        }]
                }]
                    ,'common' : 1})
            self.assertEqual(response.status_code, 200)

    def test_roomfilter_invalid_room_view(self):
        client   = Client()
        response = client.get('/rooms?city=부산')
        self.assertEqual(response.json(),{'message':'NO_ROOM_AVAILABLE'})
        self.assertEqual(response.status_code, 400)
