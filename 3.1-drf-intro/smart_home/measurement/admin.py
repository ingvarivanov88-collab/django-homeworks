from django.contrib import admin
from django.utils.html import format_html
from .models import Sensor, Measurement


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name', 'description']


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ['id', 'sensor', 'temperature', 'created_at', 'image_preview']
    list_filter = ['sensor', 'created_at']
    search_fields = ['sensor__name']
    readonly_fields = ['image_preview']
    fields = ['sensor', 'temperature', 'image', 'image_preview']  # <-- добавили image

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "Нет изображения"

    image_preview.short_description = 'Превью'