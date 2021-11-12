from django.db import models


class Category(models.Model):
    name_cat = models.CharField(max_length=50)
