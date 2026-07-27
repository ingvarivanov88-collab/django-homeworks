from django.shortcuts import render
from django.http import Http404
from .models import Book


def books_view(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'books/books_list.html', context)


def books_by_date_view(request, pub_date):
    books = Book.objects.filter(pub_date=pub_date)

    if not books.exists():
        raise Http404("Книги за эту дату не найдены")

    # Получаем все уникальные даты, сортируем по убыванию
    all_dates = Book.objects.values_list('pub_date', flat=True).distinct().order_by('pub_date')
    all_dates_list = list(all_dates)

    # Находим текущую дату в списке
    try:
        current_index = all_dates_list.index(pub_date)
    except ValueError:
        raise Http404("Дата не найдена")

    # Определяем предыдущую и следующую даты
    previous_date = all_dates_list[current_index - 1] if current_index > 0 else None
    next_date = all_dates_list[current_index + 1] if current_index < len(all_dates_list) - 1 else None

    context = {
        'books': books,
        'pub_date': pub_date,
        'previous_date': previous_date,
        'next_date': next_date,
    }
    return render(request, 'books/books_by_date.html', context)