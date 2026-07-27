from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название')
    author = models.CharField(max_length=64, verbose_name='Автор')
    pub_date = models.DateField(verbose_name='Дата публикации')

    def __str__(self):
        return f'{self.name} - {self.author}'