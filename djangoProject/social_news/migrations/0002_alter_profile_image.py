# Generated by Django 5.0.6 on 2024-06-13 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(upload_to='profiles/'),
        ),
    ]
