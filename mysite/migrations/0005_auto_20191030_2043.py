# Generated by Django 2.2.6 on 2019-10-30 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0004_articlepost_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='summary',
            field=models.TextField(),
        ),
    ]
