from django.urls import reverse
from pytils.translit import slugify
from registration_authorisation.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from hipeak_portal.settings import RATING_CHOICE


class Category(models.Model):
    category = models.CharField(max_length=25)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class Organisations(models.Model):
    name = models.CharField(max_length=100, unique=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(auto_created=True)
    description = models.TextField()
    location = models.CharField(max_length=100)
    url = models.URLField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, help_text='Contact phone number')
    category = models.ManyToManyField(Category)
    email = models.EmailField(unique=True,
                              error_messages={"unique": _("A organisation with that email already exists.")})
    in_bookmarks = models.ManyToManyField(User,
                                          through='Bookmarks', related_name='user_bookmarks')
    rating = models.ManyToManyField(User,
                                    through='Ratings', related_name='organisation_rating')
    comment = models.ManyToManyField(User,
                                     through='OrganisationsComment', related_name='organisation_comment')
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
<<<<<<< HEAD
        if all_voice:
            rating = self.rating.values_list('ratings__rating', flat=True)
            result = round(sum(rating) / all_voice, 1)
            return result
        return 0

    def in_user_bookmarks(self, username):
        exists = Bookmarks.objects.filter(organisation__name=self.name, user=username)
        if exists:
            return exists
        return None

    def get_absolute_url(self):
        return f"/tours/organisations/{self.slug}"

    def total_comments(self):
        return self.comment.count()

    class Meta:
        verbose_name = 'Організація'
        verbose_name_plural = 'Організації'


class Tours(models.Model):
    CURRENCY_CHOICE = (
        ('uah', "UAH"),
    )

    FOOD_CATEGORY_CHOICE = (
        ('room only', "RO(room only)"),
        ('half board', "HB(half board)"),
        ('full board', "FB(full board)"),
        ('all inclusive', "AI(all inclusive)")
    )

    RESIDENCE_CHOICE = (
        ("camp", "Camp"),
        ("camp|hotel", "Camp|Hotel"),
        ("hotel", "Hotel"),
    )

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    category = models.ManyToManyField(Category, related_name='tour_category',
                                      help_text="Щоб обрати декілька категорій, зажміть 'alt' або 'command'")
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    organisation = models.ForeignKey(Organisations, on_delete=models.CASCADE)
    food = models.CharField(choices=FOOD_CATEGORY_CHOICE, null=True, max_length=13)
    transfer = models.BooleanField(default=False)
    flying = models.BooleanField(default=False)
    residence = models.CharField(choices=RESIDENCE_CHOICE, null=True, max_length=17)
    price = models.PositiveBigIntegerField()
    start_date = models.DateField()
    finish_date = models.DateField()
    currency = models.CharField(choices=CURRENCY_CHOICE, null=True, max_length=3)
    rating = models.ManyToManyField(User, through='TourRatings', related_name='tour_rating')
    in_bookmarks = models.ManyToManyField(User, through='TourBookmarks', related_name='tour_bookmarks')
    comment = models.ManyToManyField(User, through='TourComments', related_name='tour_comment')
    img = models.ImageField(null=True, upload_to='tours/', blank='true', verbose_name='tours_img')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tours, self).save(*args, **kwargs)

    def total_rating(self):
        all_voice = self.rating.count()
        if all_voice:
            rating = self.rating.values_list('tourratings__rating', flat=True)
            return round(sum(rating) / all_voice, 1)
        return 0

    def get_absolute_url(self):
        # return reverse("tours", kwargs={'slug': self.slug})
        return f"/tours/{self.slug}"

    def total_comments(self):
        return self.comment.count()

    def in_user_bookmarks(self, username):
        exists = TourBookmarks.objects.filter(tour__name=self.name, user=username)
        if exists:
            return exists
        return None

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Тури'


class OrganisationsComment(models.Model):
    article_name = models.ForeignKey(Organisations, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='user')
    comment_text = models.CharField(max_length=150)
    pub_date = models.DateTimeField(auto_now_add=True)
    moderate_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Коментар організаціЇ'
        verbose_name_plural = 'Коментарі організацій'

    def __str__(self):
        return f"Tour: {self.article_name.name} | Author: {self.author}"


class TourComments(models.Model):
    article_name = models.ForeignKey(Tours, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.NOT_PROVIDED)
    comment_text = models.CharField(max_length=300)
    pub_date = models.DateTimeField(auto_now_add=True)
    moderate_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Tour: {self.article_name.name} | Author: {self.author}"

    class Meta:
        verbose_name = 'Коментар туру'
        verbose_name_plural = 'Коментарі турів'


class TourBookmarks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tour = models.ForeignKey(Tours, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Tour: {self.tour.name} | User: {self.user.username}"

    # def exist_bookmark(self):


    class Meta:
        verbose_name = 'Закладка. Тури'
        verbose_name_plural = 'Закладки. Тури'
=======
        rating = sum(self.rating.values_list('ratings__rating', flat=True))
        if all_voice:
            return round(rating / all_voice, 1)
        return 0
>>>>>>> 21a625e0fd39a6ed230266947b4b916e3dec324c


class Bookmarks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    organisation = models.ForeignKey(Organisations, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Organisation: {self.organisation.name} | User: {self.user.username}"

    class Meta:
        verbose_name = 'Закладка. Організації'
        verbose_name_plural = 'Закладки. Організації'


class TourRatings(models.Model):
    user = models.ForeignKey(User, on_delete=models.NOT_PROVIDED)
    rate_article = models.ForeignKey(Tours, on_delete=models.CASCADE, null=True)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICE, null=True)

    def __str__(self):
        return f"Tour: {self.rate_article.name} | Rating: {self.rating}"

    class Meta:
        verbose_name = 'Рейтинг туру'
        verbose_name_plural = 'Рейтинг турів'


class Ratings(models.Model):
    user = models.ForeignKey(User, on_delete=models.NOT_PROVIDED)
    rate_article = models.ForeignKey(Organisations, on_delete=models.CASCADE, null=True)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICE, null=True)

    def __str__(self):
        return f"Organisation: {self.rate_article.name} | Rating: {self.rating}"

    class Meta:
        verbose_name = 'Рейтинг організації'
        verbose_name_plural = 'Рейтинг організацій'
