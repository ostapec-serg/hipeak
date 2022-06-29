from django.contrib import admin
from tours import models


@admin.register(models.Tours)
class ToursAdmin(admin.ModelAdmin):
    list_display = ('name', 'organisation', 'pub_date', 'price')
    list_display_links = ('name', 'organisation', 'pub_date', 'price')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(models.Organisations)
class OrganisationsAdmin(admin.ModelAdmin):
    list_display = ('name', 'pub_date',)
    list_display_links = ('name', 'pub_date',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    list_display_links = ('category',)


@admin.register(models.Ratings)
class RatingsAdmin(admin.ModelAdmin):
    list_display = ('rating', 'rate_article', 'user')
    list_display_links = ('rating', 'rate_article', 'user')


@admin.register(models.TourRatings)
class TourRatingsAdmin(admin.ModelAdmin):
    list_display = ('rating', 'rate_article', 'user')
    list_display_links = ('rating', 'rate_article', 'user')


@admin.register(models.Bookmarks)
class BookmarksAdmin(admin.ModelAdmin):
    list_display = ('user', 'organisation',)
    list_display_links = ('user', 'organisation',)


@admin.register(models.TourBookmarks)
class TourBookmarksAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour',)
    list_display_links = ('user', 'tour',)


@admin.register(models.TourComments)
class TourCommentsAdmin(admin.ModelAdmin):
    list_display = ('moderate_status', 'pub_date',)
    list_display_links = ('moderate_status', 'pub_date',)


@admin.register(models.OrganisationsComment)
class OrganisationsCommentAdmin(admin.ModelAdmin):
    list_display = ('moderate_status', 'pub_date',)
    list_display_links = ('moderate_status', 'pub_date',)



