from django.contrib import admin
from django.contrib.admin import ModelAdmin

from news_blog import models


@admin.register(models.NewsCategory)
class CategoryAdmin(ModelAdmin):
    list_display = ('category', )
    list_display_links = ('category',)


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'url',)
    list_display_links = ('name',  'url',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(models.Likes)
class LikesAdmin(admin.ModelAdmin):
    list_display = ('like_date',)
    list_display_links = ('like_date',)


@admin.register(models.Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('moderate_status', 'pub_date',)
    list_display_links = ('moderate_status', 'pub_date',)

