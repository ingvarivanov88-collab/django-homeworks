from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    tags = models.ManyToManyField(Tag, through='Scope', verbose_name='Теги')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

class Scope(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='scopes')
    is_main = models.BooleanField(default=False, verbose_name='Основной тег')

    class Meta:
        verbose_name = 'Связь'
        verbose_name_plural = 'Связи'
        ordering = ['-is_main', 'tag__name']

    def __str__(self):
        return f"{self.article.title} - {self.tag.name}"