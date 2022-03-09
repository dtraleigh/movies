from django.core.management.base import BaseCommand

from movies.models import *
from movies.management.commands.functions import query_tmdb


class Command(BaseCommand):
    def handle(self, *args, **options):
        all_movies = Movie.objects.all()

        for movie in all_movies:
            tmdb_json = query_tmdb(movie.themoviedb_id)
            try:
                movie.genre_data = tmdb_json["genres"]
                movie.save()
            except Exception as e:
                print(e)
                print(f"Double check {movie}")

