from django.db import models
from tours.models import Category


class TelegramUsers(models.Model):
    user_id = models.PositiveIntegerField()
    chat_id = models.IntegerField()
    username = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    subscribe_cat = models.ManyToManyField(Category, related_name='subscribes_cat', blank=True)

    def __str__(self):
        return f"Name: {self.username} | User id: {self.user_id}"

    @staticmethod
    def user_count():
        return TelegramUsers.objects.count()

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'
