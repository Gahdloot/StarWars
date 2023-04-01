from django.db import models

# Create your models here.
from django.db import models


class Film(models.Model):
    title = models.CharField(max_length=255)
    comment_count = models.IntegerField(default=0)
    release_date = models.DateField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['clicks']


