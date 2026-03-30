from django.db import models


class Achievement(models.Model):
    title = models.CharField("Заголовок досягнення", max_length=255)
    year = models.CharField("Рік або Сезон", max_length=50, help_text="Наприклад: 2024 або Осінь 2023")
    description = models.TextField("Опис перемоги")

    # Три фото для лінійки
    image_main = models.ImageField("Головне фото (кубок/команда)", upload_to='achievements/')
    image_2 = models.ImageField("Додаткове фото 1", upload_to='achievements/', blank=True, null=True)
    image_3 = models.ImageField("Додаткове фото 2", upload_to='achievements/', blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Досягнення"
        verbose_name_plural = "Досягнення"
        ordering = ['-date_added']

    def __str__(self):
        return f"{self.year} - {self.title}"