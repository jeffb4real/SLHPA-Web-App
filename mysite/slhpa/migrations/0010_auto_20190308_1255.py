# Generated by Django 2.1.5 on 2019-03-08 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slhpa', '0009_document'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.AddField(
            model_name='photorecord',
            name='document',
            field=models.FileField(null=True, upload_to='documents/'),
        ),
    ]
