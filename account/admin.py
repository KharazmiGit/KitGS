from django.contrib import admin
from .models import GamAccount, UnsentLetter, LetterArchive


# Register your models here.
@admin.register(GamAccount)
class GamAccountAdmin(admin.ModelAdmin):
    list_display = ['username', 'desktop_ip', 'is_active']
    list_display_links = ['username']
    search_fields = ['username']
    readonly_fields = ['date_joined']


@admin.register(UnsentLetter)
class UnsentLetterAdmin(admin.ModelAdmin):
    list_display = ['user', 'letter_id', 'receiver', 'sent_time']
    list_display_links = ['user']
    search_fields = ['letter_id']


@admin.register(LetterArchive)
class LetterArchiveAdmin(admin.ModelAdmin):
    list_display = ['user', 'letter_id', 'created_at']
    search_fields = ['letter_id']
