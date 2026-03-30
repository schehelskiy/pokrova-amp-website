from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField("Назва категорії", max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField("Заголовок", max_length=250)
    # ЗМІНЕНО: тепер ManyToManyField дозволяє обирати кілька категорій
    categories = models.ManyToManyField(Category, related_name='posts', verbose_name="Категорії")
    image = models.ImageField("Головне фото", upload_to='news/')
    content = RichTextField("Текст новини")
    created_at = models.DateTimeField("Дата публікації", auto_now_add=True)
    is_published = models.BooleanField("Опубліковано", default=True)

    class Meta:
        verbose_name = "Новина"
        verbose_name_plural = "Новини"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class PostImage(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='news_gallery/', verbose_name="Додаткове фото")

    def __str__(self):
        return f"Фото для: {self.post.title}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField("Коментар")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"