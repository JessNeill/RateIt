# Generated by Django 2.2.28 on 2024-03-22 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='picture',
            field=models.ImageField(blank=True, upload_to='media/'),
        ),
    ]
