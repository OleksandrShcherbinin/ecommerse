from django.db import models


class Timestampable(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    dete_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
