# Generated by Django 2.2.6 on 2019-10-30 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0003_auto_20191030_1854'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepost',
            name='summary',
            field=models.TextField(default=None),
        ),
    ]
