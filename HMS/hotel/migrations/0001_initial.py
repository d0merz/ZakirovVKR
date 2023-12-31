# Generated by Django 3.2.18 on 2023-03-22 09:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateOfReservation', models.DateField(default=django.utils.timezone.now)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneNumber', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('salary', models.FloatField()),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventType', models.CharField(choices=[('Movie', 'Movie'), ('Theater', 'Theater'), ('Conference', 'Conference'), ('Concert', 'Concert'), ('Entertainment', 'Entertainment'), ('Live Music', 'Live Music')], max_length=20)),
                ('location', models.CharField(max_length=100)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('explanation', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('number', models.IntegerField(primary_key=True, serialize=False)),
                ('capacity', models.SmallIntegerField()),
                ('numberOfBeds', models.SmallIntegerField()),
                ('roomType', models.CharField(choices=[('King', 'King'), ('Luxury', 'Luxury'), ('Normal', 'Normal'), ('Economic', 'Economic')], max_length=20)),
                ('price', models.FloatField()),
                ('statusStartDate', models.DateField(null=True)),
                ('statusEndDate', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startTime', models.DateTimeField()),
                ('endTime', models.DateTimeField()),
                ('description', models.TextField()),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneNumber', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventAttendees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numberOfDependees', models.IntegerField(default=0)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.event')),
                ('guest', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.guest')),
            ],
        ),
        migrations.CreateModel(
            name='Dependees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('booking', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.booking')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='guest',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.guest'),
        ),
        migrations.AddField(
            model_name='booking',
            name='roomNumber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.room'),
        ),
    ]
