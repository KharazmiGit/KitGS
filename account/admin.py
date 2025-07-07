from django.contrib import admin
from .models import GamAccount

# Register your models here.
@admin.register(GamAccount)
class GamAccountAdmin(admin.ModelAdmin):
    list_display = ['username', 'desktop_ip', 'is_active']
    list_display_links = ['username']
    search_fields = ['username']
    readonly_fields = ['date_joined']