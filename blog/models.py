from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва")
    description = models.TextField(blank=True, verbose_name="Опис")

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публікації")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='articles', verbose_name="Категорія"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='articles', verbose_name="Автор"
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="Автор")
    text = models.TextField(verbose_name="Текст")
    comment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата коментування")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name="Стаття")

    def __str__(self):
        return f"{self.author}: {self.text[:30]}"
