# Generated by Django 3.0.7 on 2020-06-29 19:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0022_auto_20200627_0651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection_finance',
            name='loan_emi_received_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='deposits_table',
            name='account_opening_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
