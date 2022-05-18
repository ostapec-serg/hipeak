from django.contrib.auth.models import User
from django.db import models


class NewsCategory(models.Model):
    categories = models.CharField(max_length=100, verbose_name="news_categories")

    def __str__(self):
        return self.categories


class News(models.Model):
    categories = models.ForeignKey(NewsCategory, on_delete=models.CASCADE)
    publication_datetime = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=250, verbose_name="news_name")
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name="news_description")
    url = models.URLField(null=True)
    author = models.CharField(max_length=80, verbose_name="news_author", null=True)
    video = models.CharField(max_length=350, null=True)
    update_time = models.DateTimeField(auto_now=True)
    news_img = models.ImageField(null=True, upload_to='images/',
                                 blank='true', verbose_name='image')
    is_active = models.BooleanField(default=False)
    like = models.ManyToManyField(User, through='Likes', related_name='liked_news')
    comment = models.ManyToManyField(User, through='Comments', related_name='comment_news')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/news-blog/{self.slug}"

    def total_likes(self):
        return self.like.count()

    def total_comments(self):
        return self.comment.count()


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"News: {self.news.name} | User: {self.user.username} | Date: {self.like_date}"


class Comments(models.Model):
    news_name = models.ForeignKey(News, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=300)
    pub_date = models.DateTimeField(auto_now_add=True)
    moderate_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.news_name} | {self.author}"
