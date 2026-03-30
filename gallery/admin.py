from django.contrib import admin
from .models import PhotoAlbum, Photo

# Цей клас дозволяє додавати фото прямо на сторінці альбому
class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1  # Скільки порожніх полів для фото показувати відразу

@admin.register(PhotoAlbum)
class PhotoAlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'count_photos')
    inlines = [PhotoInline]  # Підключаємо вбудовані фото

    def count_photos(self, obj):
        return obj.photos.count()
    count_photos.short_description = 'Кількість фото'

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('album', 'uploaded_at')