# Generated by Django 3.0.3 on 2021-02-04 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myInsta', '0018_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likes',
            old_name='user',
            new_name='curr_user',
        ),
        migrations.RemoveField(
            model_name='likes',
            name='likes',
        ),
    ]
