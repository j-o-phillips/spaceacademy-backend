# Generated by Django 4.2.7 on 2023-11-21 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn_app', '0005_lockedcards'),
        ('game_app', '0004_rename_user_profile_hangar_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hangar',
            name='profile',
        ),
        migrations.AddField(
            model_name='hangar',
            name='profile',
            field=models.ManyToManyField(to='learn_app.userprofile'),
        ),
    ]
