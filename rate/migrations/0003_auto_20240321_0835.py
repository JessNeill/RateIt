# Generated by Django 2.2.28 on 2024-03-21 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0002_auto_20240321_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_rating',
            name='rating',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='movie_rating',
            name='rating',
            field=models.IntegerField(),
        ),
    ]