# Generated by Django 3.2.18 on 2023-03-26 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0012_auto_20230323_0346'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='image',
            field=models.ImageField(blank=True, upload_to='rooms/', verbose_name='Картинка'),
        ),
    ]