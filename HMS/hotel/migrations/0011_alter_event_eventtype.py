# Generated by Django 3.2.18 on 2023-03-23 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0010_auto_20230323_0315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='eventType',
            field=models.CharField(choices=[('Фильм', 'Фильм'), ('Театр', 'Театр'), ('Конференция', 'Конференция'), ('Концерт', 'Концерт'), ('Развлечения', 'Развлечения'), ('Живая музыка', 'Живая музыка')], max_length=20),
        ),
    ]
