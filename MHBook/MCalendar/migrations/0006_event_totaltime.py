# Generated by Django 5.1.2 on 2024-11-02 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MCalendar', '0005_rename_allotedtime_event_finishtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='totalTime',
            field=models.IntegerField(default=0),
        ),
    ]