# Generated by Django 5.1.2 on 2024-11-03 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MCalendar', '0009_merge_20241103_1330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billing',
            name='supervisor',
        ),
        migrations.AddField(
            model_name='billing',
            name='supervisor',
            field=models.CharField(default='Temporary', max_length=64),
            preserve_default=False,
        ),
    ]