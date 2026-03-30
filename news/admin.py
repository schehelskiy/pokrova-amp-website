from django.contrib import admin
from .models import Post, Category, PostImage, Comment


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 3


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # ЗМІНЕНО: тепер 'categories' замість 'category'
    list_display = ('title', 'created_at', 'is_published')

    # Додаємо зручний інтерфейс для вибору багатьох категорій
    filter_horizontal = ('categories',)

    # ЗМІНЕНО: фільтр тепер теж по 'categories'
    list_filter = ('categories', 'is_published')

    search_fields = ('title', 'content')
    inlines = [PostImageInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Comment)