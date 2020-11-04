# Generated by Django 3.0.7 on 2020-06-12 19:59

import cropperjs.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0016_auto_20200610_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basic_details',
            name='id_photograph1',
            field=cropperjs.models.CropperImageField(upload_to='users/images'),
        ),
        migrations.AlterField(
            model_name='basic_details',
            name='id_photograph2',
            field=cropperjs.models.CropperImageField(blank=True, null=True, upload_to='users/images'),
        ),
        migrations.AlterField(
            model_name='basic_details',
            name='id_photograph3',
            field=cropperjs.models.CropperImageField(blank=True, null=True, upload_to='users/images'),
        ),
        migrations.AlterField(
            model_name='basic_details',
            name='id_photograph4',
            field=cropperjs.models.CropperImageField(blank=True, null=True, upload_to='users/images'),
        ),
        migrations.AlterField(
            model_name='basic_details',
            name='signature',
            field=cropperjs.models.CropperImageField(upload_to='users/images'),
        ),
        migrations.AlterField(
            model_name='basic_details',
            name='thumb_impression',
            field=cropperjs.models.CropperImageField(blank=True, null=True, upload_to='users/images'),
        ),
        migrations.AlterField(
            model_name='employee_interview',
            name='ref_id_1',
            field=cropperjs.models.CropperImageField(blank=True, null=True, upload_to='users/images'),
        ),
        migrations.AlterField(
            model_name='employee_interview',
            name='ref_id_2',
            field=cropperjs.models.CropperImageField(blank=True, null=True, upload_to='users/images'),
        ),
        migrations.AlterField(
            model_name='employee_interview',
            name='referal_photograph',
            field=cropperjs.models.CropperImageField(blank=True, null=True, upload_to='users/images'),
        ),
        migrations.AlterField(
            model_name='employee_interview',
            name='referal_signature',
            field=cropperjs.models.CropperImageField(blank=True, null=True, upload_to='users/images'),
        ),
        migrations.AlterField(
            model_name='employee_interview',
            name='upload_bank_passbook',
            field=cropperjs.models.CropperImageField(blank=True, null=True, upload_to='users/images'),
        ),
        migrations.AlterField(
            model_name='employee_interview',
            name='upload_cheque',
            field=cropperjs.models.CropperImageField(blank=True, null=True, upload_to='users/images'),
        ),
        migrations.AlterField(
            model_name='employee_interview',
            name='upload_id_1',
            field=cropperjs.models.CropperImageField(blank=True, null=True, upload_to='users/images'),
        ),
        migrations.AlterField(
            model_name='employee_interview',
            name='upload_id_2',
            field=cropperjs.models.CropperImageField(blank=True, null=True, upload_to='users/images'),
        ),
        migrations.AlterField(
            model_name='employee_interview',
            name='upload_stamp_paper',
            field=cropperjs.models.CropperImageField(blank=True, null=True, upload_to='users/images'),
        ),
        migrations.AlterField(
            model_name='finance_table',
            name='cheque_photograph',
            field=cropperjs.models.CropperImageField(upload_to='users/images'),
        ),
        migrations.AlterField(
            model_name='finance_table',
            name='stamp_photograph',
            field=cropperjs.models.CropperImageField(upload_to='users/images'),
        ),
        migrations.AlterField(
            model_name='gaurantor',
            name='photograph',
            field=cropperjs.models.CropperImageField(upload_to='users/images'),
        ),
    ]
