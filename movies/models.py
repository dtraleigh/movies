import django.contrib.postgres.fields
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=300)
    sort_title = models.CharField(max_length=300, default=title)
    primary_release_year = models.IntegerField()
    themoviedb_id = models.IntegerField()
    imdb_id = models.CharField(max_length=50)
    poster_path = models.CharField(max_length=300)
    formats = models.ManyToManyField("Format", default=None, blank=True)
    comments = models.CharField(max_length=300, blank=True, null=True)
    genre_data = models.JSONField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    letterboxd_url_slug = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.primary_release_year})"

    def get_formats(self):
        return ", ".join([f.name for f in self.formats.all()])


class Format(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class APIUser(models.Model):
    name = models.CharField(max_length=50, unique=True)
    api_key = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Collection(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default=None, blank=True)
    movies = models.ManyToManyField("Movie", default=None, blank=True)

    def __str__(self):
        return self.name
