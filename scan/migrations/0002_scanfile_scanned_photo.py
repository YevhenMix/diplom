# Generated by Django 3.0.14 on 2021-04-17 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scanfile',
            name='scanned_photo',
            field=models.ImageField(default=None, null=True, upload_to='static/scanned_image'),
        ),
    ]
