from django.db import models


class Sensor(models.Model):
    """Модель датчика"""
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.CharField(max_length=200, blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'

    def __str__(self):
        return self.name


class Measurement(models.Model):
    """Модель измерения температуры"""
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name='measurements',
        verbose_name='Датчик'
    )
    temperature = models.FloatField(verbose_name='Температура')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время измерения')
    image = models.ImageField(
        upload_to='measurements/',
        null=True,
        blank=True,
        verbose_name='Изображение'
    )

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sensor.name} - {self.temperature}°C ({self.created_at})"