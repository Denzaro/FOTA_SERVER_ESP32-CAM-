from django.contrib import admin
from .models import ALM_Server
# Register your models here.

@admin.register(ALM_Server)
class HILSetupAdmin(admin.ModelAdmin):
    list_display = ('name', 'host')
    search_fields = ('name', 'host')
