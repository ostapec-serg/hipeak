from django.contrib import admin

from telegram_bot import models
# Register your models here.


@admin.register(models.TelegramUsers)
class TelegramUsersAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username')
    list_display_links = ('user_id', 'username')
