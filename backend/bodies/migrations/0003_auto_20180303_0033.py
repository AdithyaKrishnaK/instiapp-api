# Generated by Django 2.0.2 on 2018-03-02 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bodies', '0002_auto_20180303_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='body',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
