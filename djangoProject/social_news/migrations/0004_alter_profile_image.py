# Generated by Django 5.0.6 on 2024-06-13 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_news', '0003_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(upload_to='PICTURES/'),
        ),
    ]
