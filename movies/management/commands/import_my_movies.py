import xml.etree.ElementTree as ET

from django.core.management.base import BaseCommand

from movies.management.commands.functions import *
from movies.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        tree_movies = ET.parse("Collection_movies.xml")
        # tree_movies = ET.parse("101_dalmations_movie.xml")
        root_movies = tree_movies.getroot()

        tree_discs = ET.parse("Collection_discs.xml")
        # tree_discs = ET.parse("101_dalmations_disc.xml")
        root_discs = tree_discs.getroot()

        for movie in root_movies.iter("Movie"):
            id = movie.find("./Global")[8].text
            imdb_id = get_imdb_id_from_xml(id, root_discs)
            tmdb_json = query_tmdb_by_imdb_id(imdb_id)

            title = tmdb_json["movie_results"][0]["title"]
            year = tmdb_json["movie_results"][0]["release_date"].split("-")[0]
            poster = tmdb_json["movie_results"][0]["poster_path"]

            Movie.objects.create(title=title,
                                 primary_release_year=year,
                                 themoviedb_id=tmdb_json["movie_results"][0]["id"],
                                 imdb_id=imdb_id,
                                 poster_path=poster)

