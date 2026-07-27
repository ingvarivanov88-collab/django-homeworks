from rest_framework import generics
from .models import Sensor, Measurement
from .serializers import SensorSerializer, SensorDetailSerializer, MeasurementSerializer


class SensorListCreateView(generics.ListCreateAPIView):
    """Список датчиков и создание нового"""
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """Получение и обновление датчика"""
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


class MeasurementCreateView(generics.CreateAPIView):
    """Создание нового измерения"""
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer