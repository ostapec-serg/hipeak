from django.contrib import admin
from django.contrib.admin import ModelAdmin

from news_blog import models


@admin.register(models.NewsCategory)
class CategoryAdmin(ModelAdmin):
    list_display = ('categories', )
    list_display_links = ('categories',)


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'categories', 'author', 'url',)
    list_display_links = ('name', 'author', 'url',)


@admin.register(models.Likes)
class LikesAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Comments)
class CommentsAdmin(admin.ModelAdmin):
    pass

