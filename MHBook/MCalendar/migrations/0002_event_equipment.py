# Generated by Django 5.1.2 on 2024-10-21 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MCalendar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='equipment',
            field=models.CharField(default='Not specified', max_length=100),
        ),
    ]