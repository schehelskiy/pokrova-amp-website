from django.db import models

class FanPhoto(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок фото")
    image = models.ImageField(upload_to='fan_zone/', verbose_name="Фото")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Фото фан-зони"
        verbose_name_plural = "Фото фан-зони"

    def __str__(self):
        return self.title