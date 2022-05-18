from django.contrib import admin
from tours import models
# Register your models here.


@admin.register(models.Ratings)
class RatingsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Organisations)
class OrganisationsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Bookmarks)
class BookmarksAdmin(admin.ModelAdmin):
    pass