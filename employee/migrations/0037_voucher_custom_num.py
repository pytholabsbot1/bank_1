# Generated by Django 3.0.7 on 2020-11-14 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0036_auto_20200809_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='custom_num',
            field=models.BooleanField(default=False),
        ),
    ]
