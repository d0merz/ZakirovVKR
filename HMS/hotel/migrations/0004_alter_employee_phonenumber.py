# Generated by Django 3.2.18 on 2023-03-22 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0003_alter_event_eventtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='phoneNumber',
            field=models.IntegerField(unique=True),
        ),
    ]