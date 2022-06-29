from registration_authorisation.models import User
from django.db import models
from pytils.translit import slugify


class NewsCategory(models.Model):
    category = models.CharField(max_length=100,
                                verbose_name="Категорії новин")

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class News(models.Model):
    category = models.ManyToManyField(NewsCategory, verbose_name="Категорії")
    pub_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=250, verbose_name="Назва")
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name="Опис")
    url = models.URLField(null=True)
    video = models.CharField(max_length=350, null=True, blank=True)
    news_img = models.ImageField(null=True, upload_to='images/',
                                 blank='true', verbose_name='image')
    like = models.ManyToManyField(User, through='Likes', related_name='liked_news')
    comment = models.ManyToManyField(User, through='Comments', related_name='comment_news')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(News, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/news-blog/{self.slug}"

    def total_likes(self):
        return self.like.count()

    def total_comments(self):
        return self.comment.count()

    class Meta:
        verbose_name = 'Новина'
        verbose_name_plural = 'Новини'


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"News: {self.news.name} | User: {self.user.username} | Date: {self.like_date}"

    class Meta:
        verbose_name = 'Вподобайка'
        verbose_name_plural = 'Вподобайки'


class Comments(models.Model):
    article_name = models.ForeignKey(News, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=300)
    pub_date = models.DateTimeField(auto_now_add=True)
    moderate_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.article_name} | {self.author}"

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'

    def get_comments(self):
        pass
