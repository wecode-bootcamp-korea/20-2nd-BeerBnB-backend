<<<<<<< HEAD
# Generated by Django 3.2.3 on 2021-05-31 11:00

=======
>>>>>>> d5fa9d3... social login
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
                ('checkin', models.DateField()),
                ('checkout', models.DateField()),
=======

                ('checkin', models.DateField()),
                ('checkout', models.DateField()),

                ('checkin', models.DateTimeField()),
                ('checkout', models.DateTimeField()),

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
