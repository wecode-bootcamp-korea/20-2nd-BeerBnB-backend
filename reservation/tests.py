import json, re, bcrypt, jwt


from django.test        import TestCase, Client

from room.models        import Room, Category, RoomAmenity, Image, Amenity, WishList, DisableDate, AbleTime
from user.models        import User,Host, Review
from reservation.models import Reservation, Status
from reservation.check  import check
from my_settings        import SECRET_KEY



class RoomwishTest(TestCase):
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
            review_user       = user1,
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
        WishList.objects.create(
            id =1,
            wish_user = user1,
            wish_room = room1
        )
  
    def test_reservation_view(self):
        client           = Client()
        reservation_data = {
                    'room'    : '양재아파트',
                    'checkin' : '2021-07-25',
                    'checkout': '2021-07-29',
                    'adult'   : '1',
                    'child'   : '1'
                    }
        token    = jwt.encode({'id': User.objects.get(id=1).id}, SECRET_KEY, algorithm = 'HS256')
        headers  = {"HTTP_Authorization": token}
        response = client.post('/reservation',json.dumps(reservation_data), **headers,content_type='application/json')
        self.assertEqual(response.json(),{'MESSAGE':'reservation success'})
        self.assertEqual(response.status_code, 200)

    def test_reservation_date_error_view(self):
        client           = Client()
        reservation_data = {
                    'room'    : '양재아파트',
                    'checkin' : '2021-06-08',
                    'checkout': '2021-06-29',
                    'adult'   : '1',
                    'child'   : '1'
                    }
        token    = jwt.encode({'id': User.objects.get(id=1).id}, SECRET_KEY, algorithm = 'HS256')
        headers  = {"HTTP_Authorization": token}
        response = client.post('/reservation',json.dumps(reservation_data), **headers,content_type='application/json')
        self.assertEqual(response.json(),{'MESSAGE':'not_available_date'})
        self.assertEqual(response.status_code, 400)

    def test_reservation_capacity_error_view(self):
        client           = Client()
        reservation_data = {
                    'room'    : '양재아파트',
                    'checkin' : '2021-07-22',
                    'checkout': '2021-07-29',
                    'adult'   : '3',
                    'child'   : '1'
                    }
        token    = jwt.encode({'id': User.objects.get(id=1).id}, SECRET_KEY, algorithm = 'HS256')
        headers  = {"HTTP_Authorization": token}
        response = client.post('/reservation',json.dumps(reservation_data), **headers,content_type='application/json')
        self.assertEqual(response.json(),{'MESSAGE':'Max capacity is overed'})
        self.assertEqual(response.status_code, 400)

    def test_reservation_name_error_view(self):
        client           = Client()
        reservation_data = {
                    'room'    : 'asdf',
                    'checkin' : '2021-07-22',
                    'checkout': '2021-07-29',
                    'adult'   : '3',
                    'child'   : '1'
                    }
        token    = jwt.encode({'id': User.objects.get(id=1).id}, SECRET_KEY, algorithm = 'HS256')
        headers  = {"HTTP_Authorization": token}
        response = client.post('/reservation',json.dumps(reservation_data), **headers,content_type='application/json')
        self.assertEqual(response.json(),{'MESSAGE':'roomname_not_available'})
        self.assertEqual(response.status_code, 400)
