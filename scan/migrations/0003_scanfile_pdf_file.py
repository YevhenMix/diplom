# Generated by Django 3.0.14 on 2021-04-19 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scan', '0002_scanfile_scanned_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='scanfile',
            name='pdf_file',
            field=models.FileField(default=None, null=True, upload_to='static/pdf_files'),
        ),
    ]
