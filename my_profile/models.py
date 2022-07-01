from django.db import models
from django.urls import reverse_lazy

from pytils.translit import slugify
from phonenumber_field.modelfields import PhoneNumberField

from registration_authorisation.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Користувач')
    slug = models.SlugField(auto_created=True)
    photo = models.ImageField(upload_to='profile_img/',
                              blank=True, null=True, verbose_name='Фото профілю')
    phone = PhoneNumberField(blank=True, help_text='В форматі(+12(345)6789 123) ', verbose_name='Номер телефону')
    bio = models.CharField(max_length=160, blank=True, null=True, verbose_name='Біографія',
                           help_text='Максимум 200 символів')
    birthday = models.DateField(null=True, blank=True, verbose_name='Дата народження',
                                help_text='В форматі дд.мм.рр.!')
    email_subscribe = models.BooleanField(default=True, verbose_name='Підписка на почтову розсилку')

    def save(self, *args, **kwargs):
        """Auto save slug"""
        self.slug = slugify(self.user)
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        """Return absolute url """
        return reverse_lazy("profile:profile", kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Прфіль'
        verbose_name_plural = 'Профілі'
