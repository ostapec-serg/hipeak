from django.urls import reverse, reverse_lazy
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
    slug = models.SlugField(auto_created=True, max_length=150)
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
        """Auto save slug"""
        self.slug = slugify(self.name)
        super(Organisations, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def total_bookmarks(self):
        """Return total organisation in_bookmarks. int()"""
        return self.in_bookmarks.count()

    def total_rating(self):
        """Return rating of the organisation. int()"""
        all_voice = self.rating.count()
        if all_voice:
            rating = self.rating.values_list('ratings__rating', flat=True)
            return round(sum(rating) / all_voice, 1)

    def in_user_bookmarks(self, username):
        """Check organisation in request.user bookmarks"""
        exists = Bookmarks.objects.filter(organisation__name=self.name, user=username)
        if exists:
            return exists

    def get_non_parent_comments(self):
        """Return list of comments who didn't have 'parent' """
        return self.organisationscomment_set.filter(parent__isnull=True)

    def get_absolute_url(self):
        """Return absolute url """
        return reverse_lazy("tours:organisation_detail", kwargs={'slug': self.slug})

    def total_comments(self):
        """Return total organisation comments. int()"""
        return self.organisationscomment_set.count()

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
    slug = models.SlugField(unique=True, max_length=150)
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
        """Auto save slug"""
        self.slug = slugify(self.name)
        super(Tours, self).save(*args, **kwargs)

    def total_rating(self):
        """Return rating of the tour. int()"""
        all_voice = self.rating.count()
        if all_voice:
            rating = self.rating.values_list('tourratings__rating', flat=True)
            return round(sum(rating) / all_voice, 1)

    def get_absolute_url(self):
        """Return absolute url """
        return reverse_lazy("tours:detail", kwargs={'slug': self.slug})

    def total_comments(self):
        """Return total tour comments. int()"""
        return self.tourcomments_set .count()

    def get_non_parent_comments(self):
        """Return list of comments who didn't have 'parent' """
        return self.tourcomments_set.filter(parent__isnull=True)

    def in_user_bookmarks(self, username):
        """Check tour in request.user bookmarks"""
        exists = TourBookmarks.objects.filter(tour__name=self.name, user=username)
        if exists:
            return exists

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Тури'


class OrganisationsComment(models.Model):
    article_name = models.ForeignKey(Organisations, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True)
    comment_text = models.CharField(max_length=150)
    pub_date = models.DateTimeField(auto_now_add=True)
    moderate_status = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL,
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'Коментар організаціЇ'
        verbose_name_plural = 'Коментарі організацій'

    def __str__(self):
        return f"Tour: {self.article_name.name} | Author: {self.author}"


class TourComments(models.Model):
    article_name = models.ForeignKey(Tours, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True)
    comment_text = models.CharField(max_length=300)
    pub_date = models.DateTimeField(auto_now_add=True)
    moderate_status = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL,
        blank=True, null=True
    )

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

    class Meta:
        verbose_name = 'Закладка. Тури'
        verbose_name_plural = 'Закладки. Тури'


class Bookmarks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    organisation = models.ForeignKey(Organisations, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Organisation: {self.organisation.name} | User: {self.user.username}"

    class Meta:
        verbose_name = 'Закладка. Організації'
        verbose_name_plural = 'Закладки. Організації'


class TourRatings(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True)
    rate_article = models.ForeignKey(Tours, on_delete=models.CASCADE, null=True)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICE, null=True)

    def __str__(self):
        return f"Tour: {self.rate_article.name} | Rating: {self.rating}"

    class Meta:
        verbose_name = 'Рейтинг туру'
        verbose_name_plural = 'Рейтинг турів'


class Ratings(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True)
    rate_article = models.ForeignKey(Organisations, on_delete=models.CASCADE, null=True)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICE, null=True)

    def __str__(self):
        return f"Organisation: {self.rate_article.name} | Rating: {self.rating}"

    class Meta:
        verbose_name = 'Рейтинг організації'
        verbose_name_plural = 'Рейтинг організацій'
