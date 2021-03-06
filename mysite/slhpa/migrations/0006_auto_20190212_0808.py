# Generated by Django 2.1.5 on 2019-02-12 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slhpa', '0005_auto_20190201_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photorecord',
            name='address',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='photorecord',
            name='contributor',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='photorecord',
            name='geo_coord_UTM',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='photorecord',
            name='geo_coord_original',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='photorecord',
            name='period_date',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='photorecord',
            name='subject',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='photorecord',
            name='verified_gps_coords',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
