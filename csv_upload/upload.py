import csv, os
import googlemaps

from django.core.wsgi   import get_wsgi_application
from faker              import Faker # 패키지 설치! (pip install Faker)
from user.models        import *
from room.models        import *
from reservation.models import * 
#*.csv 파일을 upload 파일과 동일 라인 공간에 둔다 / 각 app의 model을 가져온다

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beerbnb.settings") 
# django.setup()
#장고 외부 파일이기 때문에, 장고 내 나의 프로젝트에 연결

# *.csv 쌓을 때 빈공간없이 정확히 쌓자
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beerbnb.settings")

def test():
    print('test')

def user_load():
    with open('user.csv') as user_file: #*.csv 파일을 upload 파일과 동일 라인 공간에 두기 때문에 user.csv 가능
        user_rows = csv.reader(user_file, delimiter=';') # 구분자를 ,에서 ;로 바꾼다
        next(user_rows, None) #첫 줄 뛰고 가져온다
        for user_row in user_rows: #csv data 입력이 업데이트 될 수 있어서 반드시 update_or_create 사용한다
            update, _ = User.objects.update_or_create(
                email        = user_row[0],
                phone_number = user_row[1],
                sex          = user_row[2],
                birthday     = user_row[3],
                password     = user_row[4],
                first_name   = user_row[5],
                last_name    = user_row[6],
                profile_url  = user_row[7],
                social_id    = None,
                is_allowed   = user_row[9]
            )
            update.save()

def host_load():    
    with open('host.csv') as host_file:
        host_rows = csv.reader(host_file, delimiter=';')
        next(host_rows, None)
        for host_row in host_rows:
            user_id = User.objects.get(email=host_row[0]).id
            update, _ = Host.objects.update_or_create(
                user_id  = user_id,
                is_super = host_row[1]
            )
            update.save()

def amenity_load():
    with open('amenity.csv') as amenity_file:
        amenity_rows = csv.reader(amenity_file, delimiter=';')
        next(amenity_rows, None)
        for amenity_row in amenity_rows:
            update,_ = Amenity.objects.update_or_create(
                name      = amenity_row[1],
                image     = amenity_row[2]
                )
            update.save()

gmaps = googlemaps.Client(key='AIzaSyDmPGt-ilBqbJyeKoKCQ6oKpiSO46onFEA')

def room_load():
    with open('room.csv') as room_file:
        room_rows = csv.reader(room_file,delimiter=';')
        next(room_rows, None)
        for room_row in room_rows:
            update,_ = Room.objects.update_or_create(
                name         = room_row[0],
                city         = room_row[1],
                price        = room_row[2],
                capacity     = room_row[3],
                latitude     = gmaps.geocode((room_row[4]), language='ko')[0]['geometry']['location']['lat'],
                longtitude    = gmaps.geocode((room_row[4]), language='ko')[0]['geometry']['location']['lng'],
                is_refund    = room_row[5],
                min_date     = room_row[6],
                category_id  = Category.objects.get(name=room_row[10]).id,
                host_id      = Host.objects.get(user__email=room_row[9]).id,
                able_time_id = AbleTime.objects.get(checkin=room_row[7],checkout=room_row[8]).id,
                disable_date_id = None
            )
            update.save()

def room_amenity_load():
    with open('amenity.csv') as amenity_file:
        amenity_rows = csv.reader(amenity_file,delimiter=';')
        next(amenity_rows, None)
        for amenity_row in amenity_rows:
            update,_ = RoomAmenity.objects.update_or_create(
                room_id    = Room.objects.get(name=amenity_row[0]).id,
                amenity_id = Amenity.objects.get(name=amenity_row[1]).id
                )
            update.save()

def category_load():
    with open('category.csv') as category_file:
        category_rows = csv.reader(category_file,delimiter=';')
        next(category_rows, None)
        for category_row in category_rows:
            update,_ = Category.objects.update_or_create(
                name = category_row[0]
                )
            update.save()

def abletime_load():
    with open('room.csv') as room_file:
        room_rows = csv.reader(room_file,delimiter=';')
        next(room_rows, None)
        for room_row in room_rows:
            update,_= AbleTime.objects.update_or_create(
                checkin = room_row[7],
                checkout= room_row[8]
            )
            update.save()

def image_load():
    with open('roomimage.csv') as image_file:
        image_rows = csv.reader(image_file,delimiter=';')
        next(image_rows, None)
        for image_row in image_rows:
            update,_= Image.objects.update_or_create(
                room_id = Room.objects.get(name=image_row[0]).id,
                url     = image_row[1]
            )
            update.save()

def review_load():
    with open('review.csv') as review_file:
        review_rows = csv.reader(review_file,delimiter=';')
        next(review_rows, None)
        for review_row in review_rows:
            update,_= Review.objects.update_or_create(
                comment = None,
                cleanliness = review_row[3],
                communication = review_row[4],
                checkin = review_row[5],
                accuracy=review_row[6],
                location=review_row[7],
                cost_effectivenes = review_row[8],
                review_room_id = Room.objects.get(name=review_row[0]).id,
                review_user_id = User.objects.get(email=review_row[1]).id
            )
            update.save()

def status_load():
    with open('reservation.csv') as reservation_file:
        reservation_rows = csv.reader(reservation_file,delimiter=';')
        next(reservation_rows, None)
        for reservation_row in reservation_rows:
            update,_= Status.objects.update_or_create(
                status = reservation_row[2]
            )
            update.save()

def reservation_load():
    with open('reservation.csv') as reservation_file:
        reservation_rows = csv.reader(reservation_file,delimiter=';')
        next(reservation_rows, None)
        for reservation_row in reservation_rows:
            update,_= Reservation.objects.update_or_create(
                user_id = User.objects.get(email=reservation_row[0]).id,
                room_id = Room.objects.get(name=reservation_row[1]).id,
                status_id = Status.objects.get(status=reservation_row[2]).id,
                checkin=reservation_row[3],
                checkout=reservation_row[4]
            )
            update.save()

def data_load():
    user_load()
    host_load()
    category_load()
    amenity_load()
    abletime_load()
    room_load()
    room_amenity_load()
    image_load()
    review_load()
    status_load()
    reservation_load()
#함수개별로(테이블 개별로) csv 업데이트 가능하고, 한번에도 가능하다, 그러나 함수 순서 신경써서 가장 먼저 채워야할 함수부터 진행시킨다
#shell에서 import upload 혹은 from upload import * 해서 함수 실행한다 / .py 확장자는 쓰지 않는다!!!!

if __name__ == '__main__':
    test()