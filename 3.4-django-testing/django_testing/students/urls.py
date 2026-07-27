from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CoursesViewSet  # <-- обрати внимание на 's' в конце

router = DefaultRouter()
router.register(r'courses', CoursesViewSet)  # <-- тоже с 's'

urlpatterns = [
    path('', include(router.urls)),
]