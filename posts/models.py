from django.db import models
from categories.models import Category
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    title_post = models.CharField(max_length=255, verbose_name='Title')
    author_post = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_post = models.DateTimeField(default=timezone.now)
    content_post = models.TextField()
    excerpt_post = models.TextField()
    category_post = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    image_post = models.ImageField(
        upload_to='post_img/%y/%m/%d', blank=True, null=True)
    published_post = models.BooleanField(default=False)

    def __str__(self):
        return self.title_post
