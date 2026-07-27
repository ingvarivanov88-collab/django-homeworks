from django.contrib import admin
from .models import Article, Tag, Scope

class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 1

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
    list_display = ['title', 'published_at']
    list_filter = ['published_at']
    search_fields = ['title', 'text']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']