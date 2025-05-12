from django.db import models

from utils.model_behaviour import Timestampable


class Product(Timestampable):
    title = models.CharField(max_length=255, verbose_name='Tile')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug')
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.title
