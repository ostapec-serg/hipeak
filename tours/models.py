from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from phone_field import PhoneField


class Category(models.Model):
    category = models.CharField(max_length=25)

    def __str__(self):
        return self.category


class Organisations(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=300)
    date_added = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    in_bookmarks = models.ManyToManyField(User, through='Bookmarks', related_name='user_bookmarks')
    category = models.ManyToManyField(Category)
    rating = models.ManyToManyField(User, through='Ratings', related_name='organisation_rating')
    email = models.EmailField(unique=True)
    img = models.ImageField(null=True, upload_to='organisations/',
                            blank='true', verbose_name='organisation_img')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Organisations, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def total_bookmarks(self):
        return self.in_bookmarks.count()

    def total_rating(self):
        all_voice = self.rating.count()
        rating = sum(self.rating.values_list('ratings__rating', flat=True))
        if all_voice:
            return round(rating / all_voice, 1)
        return 0


class Bookmarks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    organisation = models.ForeignKey(Organisations, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"News: {self.organisation.name} | User: {self.user.username}"


class Ratings(models.Model):
    RATING_CHOICE = (
        (1, "Ok"),
        (2, "Fine"),
        (3, "Good"),
        (4, "Nice"),
        (5, "Amazing")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisations, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICE, null=True)

    def __str__(self):
        return f"News: {self.organisation.name} | Rating: {self.rating}"
