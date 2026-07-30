from django.shortcuts import render
from django.db.models import Prefetch
from .models import Article, Scope


def articles_list(request):
    template = 'articles/news.html'

    articles = Article.objects.all().order_by('-published_at').prefetch_related(
        Prefetch('scopes', queryset=Scope.objects.select_related('tag').order_by('-is_main', 'tag__name'))
    )

    context = {
        'articles': articles,
    }

    return render(request, template, context)