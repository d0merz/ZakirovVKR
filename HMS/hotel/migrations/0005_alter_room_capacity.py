# Generated by Django 3.2.18 on 2023-03-22 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0004_alter_employee_phonenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='capacity',
            field=models.SmallIntegerField(null=True),
        ),
    ]