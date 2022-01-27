from django.core.management.base import BaseCommand

from movies.models import Movie


class Command(BaseCommand):
    def handle(self, *args, **options):
        movies = Movie.objects.all()

        for movie in movies:
            letterboxd_url_slug = ""
            for char in movie.title:
                if char == " ":
                    letterboxd_url_slug += "-"
                elif char == "-":
                    letterboxd_url_slug += "-"
                elif not char.isalnum():
                    letterboxd_url_slug += ""
                else:
                    letterboxd_url_slug += char.lower()
            movie.letterboxd_url_slug = letterboxd_url_slug
            movie.save()
