from django.core.management.base import BaseCommand

from movies.models import *
from movies.management.commands.functions import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        ma = Format.objects.get(name="ma")
        amz = Format.objects.get(name="amz")
        g_play = Format.objects.get(name="g_play")
        vudu = Format.objects.get(name="vudu")
        itunes = Format.objects.get(name="apple_tv")
        all_movies = Movie.objects.all()

        for movie in all_movies:
            if ma in movie.formats.all():
                movie.formats.add(amz)
                movie.formats.add(g_play)
                movie.formats.add(vudu)
                movie.formats.add(itunes)
