# Generated by Django 2.2.28 on 2024-03-22 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.CharField(choices=[('Fantasy', 'Fantasy'), ('Tragedy', 'Tragedy'), ('Others', 'Others')], max_length=50),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.CharField(choices=[('Crime', 'Crime'), ('Thriller', 'Thriller'), ('Others', 'Others')], max_length=50),
        ),
    ]