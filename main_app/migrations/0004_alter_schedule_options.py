# Generated by Django 4.0.5 on 2022-06-08 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_schedule_day_alter_schedule_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedule',
            options={'ordering': ['day']},
        ),
    ]
