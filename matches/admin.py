from django.contrib import admin
from .models import Match, TournamentTable, MatchVote

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('team_type', 'display_teams', 'date', 'league', 'is_finished', 'score_display')
    list_filter = ('team_type', 'league', 'is_finished', 'date')
    search_fields = ('home_team', 'away_team')

    filter_horizontal = ('squad',)

    fieldsets = (
        ('Команди', {
            # === ДОДАНО ПОЛЯ ШИРИНИ ЛОГОТИПІВ ===
            # Вони йдуть одразу після завантаження самого логотипу
            'fields': (
                'team_type',
                ('home_team', 'home_logo', 'home_logo_width'),
                ('away_team', 'away_logo', 'away_logo_width')
            )
        }),
        ('Склад команди', {
            'fields': ('squad',),
            'description': 'Оберіть гравців, які брали участь у матчі, щоб за них можна було голосувати.'
        }),
        ('Деталі матчу', {
            'fields': ('date', 'stadium', 'stadium_link', 'league')
        }),
        ('Медіа та Умови', {
            'fields': ('weather', 'broadcast_link'),
            'classes': ('collapse',),
        }),
        ('Оформлення', {
            'fields': ('background_image',)
        }),
        ('Результат', {
            'fields': (
                'is_finished',
                ('home_score', 'away_score'),
                ('home_scorers', 'away_scorers')
            )
        }),
    )

    def display_teams(self, obj):
        return f"{obj.home_team} vs {obj.away_team}"

    display_teams.short_description = 'Матч'

    def score_display(self, obj):
        if obj.is_finished:
            return f"{obj.home_score} : {obj.away_score}"
        return "- : -"

    score_display.short_description = 'Рахунок'


@admin.register(MatchVote)
class MatchVoteAdmin(admin.ModelAdmin):
    list_display = ('match', 'player', 'user', 'created_at')
    list_filter = ('match',)


@admin.register(TournamentTable)
class TournamentTableAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'league', 'games_played', 'wins', 'draws', 'losses', 'points', 'is_our_team')
    list_filter = ('league', 'is_our_team')
    search_fields = ('team_name',)
    list_editable = ('games_played', 'wins', 'draws', 'losses', 'points')

    fieldsets = (
        ('Основна інформація', {
            # === ДОДАНО ПОЛЕ ШИРИНИ ЛОГОТИПУ В ТАБЛИЦІ ===
            'fields': ('team_name', 'league', 'team_logo', 'logo_width', 'is_our_team')
        }),
        ('Статистика', {
            'fields': (('games_played', 'wins', 'draws', 'losses'), 'points')
        }),
    )