from django.contrib import admin

from .models import ScanFile


@admin.register(ScanFile)
class ScanAdmin(admin.ModelAdmin):
    pass
