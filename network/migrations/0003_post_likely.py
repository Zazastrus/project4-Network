# Generated by Django 4.2 on 2023-08-21 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likely',
            field=models.IntegerField(default=0),
        ),
    ]
