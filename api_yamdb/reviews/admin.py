from django.contrib import admin

from api_yamdb.settings import EMPTY_VALUE_DISPLAY

from .models import Category, Comment, Genre, Review, Title


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review_id', 'text', 'author', 'pub_date')
    search_filter = ('text',)
    list_filter = ('pub_date', 'author', 'review_id',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category', 'description')
    search_fields = ('name',)
    list_filter = ('category',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'score')
    search_fields = ('text',)
    list_filter = ('pub_date', 'score',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)
    empty_value_display = EMPTY_VALUE_DISPLAY
