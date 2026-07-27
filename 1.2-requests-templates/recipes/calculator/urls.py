from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('<str:dish_name>/', views.recipe_view, name='recipe'),
]