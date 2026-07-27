import csv
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator

def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    with open(settings.BUS_STATION_CSV, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        stations_list = list(reader)
    # Получаем номер страницы из GET-параметра (по умолчанию 1)
    page_number = request.GET.get('page', 1)

    # Создаем пагинатор (10 остановок на страницу)
    paginator = Paginator(stations_list, 10)

    # Получаем объект текущей страницы
    page = paginator.get_page(page_number)

    context = {
        'bus_stations': page,  # список остановок на текущей странице
        'page': page,  # объект страницы (для навигации)
    }
    return render(request, 'stations/bus_stations.html', context)
