# Generated by Django 3.2.18 on 2023-03-27 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0013_room_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(choices=[('Кинозал', 'Кинозал'), ('Театральный зал', 'Театральный зал'), ('Конфернцзал', 'Конфернцзал'), ('Концертный зал', 'Концертный зал'), ('Лаундж-зона', 'Лаундж-зона')], max_length=100),
        ),
    ]
