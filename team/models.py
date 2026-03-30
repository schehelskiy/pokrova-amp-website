from django.db import models


class Player(models.Model):
    POSITION_CHOICES = [
        ('GK', 'Воротар'),
        ('DF', 'Захисник'),
        ('MF', 'Півзахисник'),
        ('FW', 'Нападник'),
        ('ADM', 'Керівництво'),
        ('COA', 'Тренер'),
        ('DOC', 'Медичний штаб'),
        ('MAS', 'Масажист'),
        ('MED', 'Медіа-служба'),
        ('SPR', 'Духовний наставник'),
    ]

    TEAM_CHOICES = [
        ('TEAM_1', 'Покрова'),
        ('TEAM_2', 'Покрова 2'),
        ('CLUB', 'Загальноклубний штаб'),
    ]

    first_name = models.CharField(max_length=50, verbose_name="Ім'я")
    last_name = models.CharField(max_length=50, verbose_name="Прізвище")
    number = models.PositiveIntegerField(null=True, blank=True, verbose_name="Номер")
    position = models.CharField(max_length=3, choices=POSITION_CHOICES, verbose_name="Позиція")
    team = models.CharField(max_length=10, choices=TEAM_CHOICES, default='TEAM_1', verbose_name="Команда")

    photo = models.ImageField(upload_to='players/', verbose_name="Фото (Портрет для карток)", blank=True)
    full_size_photo = models.ImageField(upload_to='players/full_size/', verbose_name="Фото в повний зріст (Детально)",
                                        blank=True, null=True)

    is_active = models.BooleanField(default=True, verbose_name="Активний у складі")

    matches_played = models.PositiveIntegerField(default=0, verbose_name="Матчі")
    goals = models.PositiveIntegerField(default=0, verbose_name="Голи")
    assists = models.PositiveIntegerField(default=0, verbose_name="Асисти")

    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата народження")
    bio = models.TextField(null=True, blank=True, verbose_name="Біографія")

    class Meta:
        verbose_name = "Учасник"
        verbose_name_plural = "Команда"
        ordering = ['team', 'position', 'number']

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.get_team_display()})"

    @property
    def age(self):
        import datetime
        if self.birth_date:
            today = datetime.date.today()
            return today.year - self.birth_date.year - (
                        (today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return "-"