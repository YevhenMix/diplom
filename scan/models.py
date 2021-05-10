from django.db import models


class ScanFile(models.Model):
    photo = models.ImageField(upload_to='static/image')
    scanned_photo = models.ImageField(upload_to='static/scanned_image', default=None, null=True)
    pdf_file = models.FileField(upload_to='static/pdf_files', default=None, null=True)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
