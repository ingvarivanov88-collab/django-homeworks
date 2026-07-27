from django.shortcuts import render
from django.http import Http404
from .models import Book
from datetime import datetime  # Добавляем импорт


def books_view(request):
    books = Book.objects.all()
    return render(request, 'books/books_list.html', {'books': books})


def books_by_date_view(request, pub_date):
    # Преобразуем строку из URL в объект date
    try:
        date_obj = datetime.strptime(pub_date, '%Y-%m-%d').date()
    except ValueError:
        raise Http404("Неверный формат даты")

    # Ищем книги за указанную дату
    books = Book.objects.filter(pub_date=date_obj)

    if not books.exists():
        raise Http404("Книги за эту дату не найдены")

    # Получаем все уникальные даты из базы (уже объекты date)
    all_dates = Book.objects.values_list('pub_date', flat=True).distinct().order_by('pub_date')
    all_dates_list = list(all_dates)

    # Ищем индекс даты как объекта
    try:
        current_index = all_dates_list.index(date_obj)  # Теперь ищем объект date
    except ValueError:
        raise Http404("Дата не найдена")

    previous_date = all_dates_list[current_index - 1] if current_index > 0 else None
    next_date = all_dates_list[current_index + 1] if current_index < len(all_dates_list) - 1 else None

    context = {
        'books': books,
        'pub_date': pub_date,
        'previous_date': previous_date,
        'next_date': next_date,
    }
    return render(request, 'books/books_by_date.html', context)