# Generated by Django 2.0.2 on 2018-03-24 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_event_website_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]