from django.contrib import admin

from my_profile.models import Profile


@admin.register(Profile)
class UserNewsRelatedAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    list_display_links = ('user', 'phone')
    prepopulated_fields = {"slug": ("user",)}

