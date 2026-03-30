from django.contrib import admin
from .models import Player

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'position', 'number', 'matches_played', 'goals', 'is_active')
    list_filter = ('team', 'position', 'is_active')
    search_fields = ('last_name', 'first_name')
    list_editable = ('is_active', 'matches_played', 'goals')

    # Групування полів для зручності в адмінці
    fieldsets = (
        ('Основна інформація', {
            'fields': ('first_name', 'last_name', 'number', 'position', 'team', 'photo', 'full_size_photo', 'is_active')
        }),
        ('Статистика', {
            'fields': ('matches_played', 'goals', 'assists')
        }),
        ('Особисті дані', {
            'fields': ('birth_date',)
        }),
        ('Додатково', {
            'fields': ('bio',),
            'description': 'Тут можна описати історію гравця та його досягнення'
        }),
    )