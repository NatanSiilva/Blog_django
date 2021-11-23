from django.db import models
from categories.models import Category
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django.conf import settings
import os


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.resize_image(self.image_post.name, 800)

    @staticmethod
    def resize_image(name_image, new_width):
        image_path = os.path.join(settings.MEDIA_ROOT, name_image)
        image = Image.open(image_path)
        width, height = image.size
        new_height = round((height * new_width) / width)

        if width <= new_width:
            image.close()
            return

        new_image = image.resize((new_width, new_height), Image.ANTIALIAS)
        new_image.save(image_path, optimize=True, quality=60)
        new_image.close()
