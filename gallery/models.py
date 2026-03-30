from django.db import models

class PhotoAlbum(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва альбому")
    description = models.TextField(blank=True, verbose_name="Опис (необов'язково)")
    cover_image = models.ImageField(upload_to='albums/covers/', verbose_name="Обкладинка альбому")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбоми"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Photo(models.Model):
    album = models.ForeignKey(PhotoAlbum, on_delete=models.CASCADE, related_name='photos', verbose_name="Альбом")
    image = models.ImageField(upload_to='albums/photos/', verbose_name="Фото")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Підпис (необов'язково)")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Фотографія"
        verbose_name_plural = "Фотографії"

    def __str__(self):
        return f"Фото в альбомі {self.album.title}"