from django.core.management.base import BaseCommand

from movies.models import *
from movies.management.commands.functions import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        all_movies = Movie.objects.all()

        for movie in all_movies:
            tmdb_json = query_tmdb(movie.themoviedb_id)
            movie.genres = str(tmdb_json["genres"]).replace("\'", "\"")
            movie.save()
