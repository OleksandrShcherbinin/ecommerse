from decimal import Decimal

from django.contrib.postgres.fields import ArrayField
from django.db import models

from utils.model_behaviour import Timestampable


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Category name')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Category slug')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(
        'store.Product', on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer_name = models.CharField(max_length=100, verbose_name='Reviewer name')
    comment = models.CharField(max_length=5000, verbose_name='Comment text')

    def __str__(self):
        return f'{self.reviewer_name}: {self.comment[:10]}'


class Product(Timestampable):
    title = models.CharField(max_length=255, verbose_name='Tile')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug')
    source_url = models.URLField(verbose_name='Source url')
    availability = models.BooleanField(default=True)
    description = models.CharField(
        max_length=10_000, verbose_name='Description',
        blank=True, default=''
    )
    old_price = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name='Price before discount'
    )
    price = models.PositiveIntegerField(verbose_name='Current price')
    discount = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True, verbose_name='Discount'
    )
    image_urls = ArrayField(
        models.URLField(verbose_name='Image source url'),
        default=list
    )
    is_images_uploaded = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, related_name='products')

    def save(
        self,
        *args,
        **kwargs
    ):
        if self.old_price:
            self.discount = Decimal(
                round((self.price / self.old_price) * 100 - 100, 2)
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Image(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='images/product', max_length=255)
    url = models.URLField(verbose_name='Image source url')
    size = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.image.url
