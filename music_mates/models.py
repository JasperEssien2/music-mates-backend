from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.URLField()
    description = models.CharField(max_length=1200)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class User(models.Model):
    google_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    image_url = models.URLField()
    favourite_artists = models.ManyToManyField(Artist, related_name='favourite_users')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
