from django.contrib import admin
from django.urls import path

from phones.views import catalog, phone_detail


urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', catalog, name='catalog'),
    path('catalog/<slug:slug>/', phone_detail, name='phone_detail'),
]