from django.contrib import admin # ОСЬ ЦЬОГО НЕ ВИСТАЧАЛО
from .models import FanPhoto

@admin.register(FanPhoto)
class FanPhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')