from django.db import models

# Create your models here.
from django.db import models


class Film(models.Model):
    title = models.CharField(max_length=255)
    episode_id = models.IntegerField()
    comment_count = models.IntegerField(default=0)
    release_date = models.DateField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['release_date']


class Comment(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def title(self):
        return self.film.title
    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        film = Film.objects.get(id=self.film.id)
        film.comment_count += 1
        film.save()
        return super().save(*args, **kwargs)