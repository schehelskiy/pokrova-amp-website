from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from team.models import Player  # Переконайся, що додаток team і модель Player існують


class Match(models.Model):
    # --- Тип команди ---
    TEAM_CHOICES = [
        ('MAIN', 'Покрова (Основна)'),
        ('SECOND', 'Покрова 2'),
    ]
    team_type = models.CharField(
        max_length=10,
        choices=TEAM_CHOICES,
        default='MAIN',
        verbose_name="Яка команда грає"
    )

    # --- Команди ---
    home_team = models.CharField(max_length=100, default="Покрова АМП", verbose_name="Господарі")
    home_logo = models.ImageField(upload_to='matches/', blank=True, null=True, verbose_name="Лого господарів")

    # === НОВЕ ПОЛЕ: Ширина логотипу господарів ===
    home_logo_width = models.PositiveIntegerField(
        default=80,
        verbose_name="Ширина лого господарів (px)",
        help_text="Змініть це число (наприклад, 60, 80, 100), щоб підігнати розмір логотипу під дизайн."
    )

    away_team = models.CharField(max_length=100, verbose_name="Гості")
    away_logo = models.ImageField(upload_to='matches/', blank=True, null=True, verbose_name="Лого гостей")

    # === НОВЕ ПОЛЕ: Ширина логотипу гостей ===
    away_logo_width = models.PositiveIntegerField(
        default=80,
        verbose_name="Ширина лого гостей (px)",
        help_text="Змініть це число (наприклад, 60, 80, 100), щоб підігнати розмір логотипу під дизайн."
    )

    # --- Інформація про матч ---
    date = models.DateTimeField(verbose_name="Дата та час матчу")
    stadium = models.CharField(max_length=200, verbose_name="Стадіон")
    league = models.CharField(max_length=100, verbose_name="Турнір", default="Чемпіонат України АМП")

    # --- Результат ---
    home_score = models.PositiveIntegerField(null=True, blank=True, verbose_name="Голи господарі")
    away_score = models.PositiveIntegerField(null=True, blank=True, verbose_name="Голи гості")
    is_finished = models.BooleanField(default=False, verbose_name="Матч завершено")

    # --- Склад та Автори голів ---
    squad = models.ManyToManyField(
        Player,
        blank=True,
        related_name='matches_in_squad',
        verbose_name="Склад команди на цей матч"
    )

    home_scorers = models.TextField(
        blank=True, null=True,
        verbose_name="Автори голів (Господарі)",
        help_text="Кожне прізвище з нового рядка"
    )
    away_scorers = models.TextField(
        blank=True, null=True,
        verbose_name="Автори голів (Гості)",
        help_text="Кожне прізвище з нового рядка"
    )

    background_image = models.ImageField(
        upload_to='matches/bg/',
        blank=True, null=True,
        verbose_name="Фонове фото матчу"
    )

    # Додаткові поля
    weather = models.CharField(max_length=100, blank=True, null=True, verbose_name="Погода (напр. +15, Ясно)")
    broadcast_link = models.URLField(blank=True, null=True, verbose_name="Посилання на трансляцію (YouTube)")
    stadium_link = models.URLField(blank=True, null=True, verbose_name="Посилання на Google Maps")

    class Meta:
        verbose_name = "Матч"
        verbose_name_plural = "Матчі"
        ordering = ['-date']

    def __str__(self):
        team_label = "Осн." if self.team_type == 'MAIN' else "П2"
        return f"[{team_label}] {self.home_team} vs {self.away_team} ({self.date.strftime('%d.%m.%Y')})"

    def get_h2h_history(self):
        """Історія зустрічей між цими двома командами"""
        return Match.objects.filter(
            Q(home_team=self.home_team, away_team=self.away_team) |
            Q(home_team=self.away_team, away_team=self.home_team),
            is_finished=True
        ).exclude(id=self.id).order_by('-date')[:5]


class MatchVote(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='votes', verbose_name="Матч")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Користувач")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='match_votes', verbose_name="Гравець")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Час голосу")

    class Meta:
        verbose_name = "Голос за гравця"
        verbose_name_plural = "Голоси"
        unique_together = ('match', 'user')  # Один юзер - один голос у матчі

    def __str__(self):
        return f"{self.user} -> {self.player} ({self.match})"


class TournamentTable(models.Model):
    LEAGUE_CHOICES = [
        ('SUPER', 'Суперліга'),
        ('FIRST', 'Перша Ліга'),
    ]

    team_name = models.CharField(max_length=100, verbose_name="Назва команди")
    team_logo = models.ImageField(upload_to='table_logos/', verbose_name="Емблема")

    # === НОВЕ ПОЛЕ: Ширина логотипу в турнірній таблиці ===
    logo_width = models.PositiveIntegerField(
        default=40,
        verbose_name="Ширина логотипу (px)",
        help_text="Стандартно 40px для таблиці. Збільште або зменште за потреби."
    )

    league = models.CharField(max_length=10, choices=LEAGUE_CHOICES, default='SUPER', verbose_name="Дивізіон")

    games_played = models.PositiveIntegerField(default=0, verbose_name="І")
    wins = models.PositiveIntegerField(default=0, verbose_name="В")
    draws = models.PositiveIntegerField(default=0, verbose_name="Н")
    losses = models.PositiveIntegerField(default=0, verbose_name="П")
    points = models.PositiveIntegerField(default=0, verbose_name="Очки")

    is_our_team = models.BooleanField(default=False, verbose_name="Наш клуб?")

    class Meta:
        verbose_name = "Рядок таблиці"
        verbose_name_plural = "Турнірна таблиця"
        ordering = ['league', '-points', '-wins']

    def __str__(self):
        return f"[{self.get_league_display()}] {self.team_name}"