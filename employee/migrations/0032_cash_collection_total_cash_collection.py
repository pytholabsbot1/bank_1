# Generated by Django 3.0.7 on 2020-07-16 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0031_auto_20200709_0600'),
    ]

    operations = [
        migrations.AddField(
            model_name='cash_collection',
            name='total_cash_collection',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
