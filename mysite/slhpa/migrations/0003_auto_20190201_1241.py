# Generated by Django 2.1.5 on 2019-02-01 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slhpa', '0002_auto_20190201_1211'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photorecord',
            old_name='resource_name',
            new_name='resource_number',
        ),
    ]