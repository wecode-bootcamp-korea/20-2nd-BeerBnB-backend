<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
# Generated by Django 3.2.3 on 2021-05-31 11:00

=======
>>>>>>> d5fa9d3... social login
=======
=======
>>>>>>> 65f2a33... dev
=======
>>>>>>> 58262ea... upload
=======
# Generated by Django 3.2.3 on 2021-05-29 13:21
=======
# Generated by Django 3.2.3 on 2021-06-01 10:06
>>>>>>> f5972cb... upload

>>>>>>> 666ebdc... auth_email
<<<<<<< HEAD
>>>>>>> b091a65... auth_email
=======
=======
# Generated by Django 3.2 on 2021-05-27 13:24

>>>>>>> a94e80e... social login
>>>>>>> 65f2a33... dev
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                ('checkin', models.DateField()),
                ('checkout', models.DateField()),
=======
=======
>>>>>>> b091a65... auth_email
=======
>>>>>>> 65f2a33... dev

                ('checkin', models.DateField()),
                ('checkout', models.DateField()),

                ('checkin', models.DateTimeField()),
                ('checkout', models.DateTimeField()),

=======
>>>>>>> 666ebdc... auth_email
=======
>>>>>>> a94e80e... social login
                ('checkin', models.DateTimeField()),
                ('checkout', models.DateTimeField()),
>>>>>>> d5fa9d3... social login
            ],
            options={
                'db_table': 'reservations',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'status',
            },
        ),
    ]
