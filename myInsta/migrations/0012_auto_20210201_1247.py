# Generated by Django 3.1.2 on 2021-02-01 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myInsta', '0011_auto_20210201_1246'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-time']},
        ),
        migrations.RemoveField(
            model_name='post',
            name='date',
        ),
        migrations.AddField(
            model_name='post',
            name='time',
            field=models.TimeField(default='12:47:09', verbose_name='Time'),
        ),
    ]
