# Generated by Django 3.2.18 on 2023-03-22 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0008_roomservices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomservices',
            name='servicesType',
            field=models.CharField(choices=[('Еда', 'Еда'), ('Уборка', 'Уборка'), ('Тех.обслуживание', 'Тех.обслуживание')], max_length=20),
        ),
    ]
