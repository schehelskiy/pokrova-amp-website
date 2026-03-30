from django.contrib import admin
from .models import Achievement

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'date_added')
    list_filter = ('year',)
    search_fields = ('title', 'description')