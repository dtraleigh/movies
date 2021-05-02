import sys

from django.core.management.base import BaseCommand

from movies.models import *
from movies.management.commands.functions import *


class Command(BaseCommand):
    help = "Adds a movie using the imdb_id.\n " \
           "Example: add_movie tt1217209 -f blu_ray,g_play,ma,amz\n" \
           "All options: vudu, plex, ma, hddvd, g_play, dvd, blu_ray, 4k, 3d, amz, itunes"

    def add_arguments(self, parser):
        parser.add_argument("imdb_id", type=str, help="IMDB ID of movie to add")

        # Optional argument
        parser.add_argument("-f", "--format", type=str, help="Add a list of formats", )
        parser.add_argument("-t", "--tv_movie", action='store_true', help="Movie is from tv_results instead", )

    def handle(self, *args, **options):
        imdb_id = options["imdb_id"]
        formats = options["format"]  # ["vudu", "plex", "ma", "hddvd", "g_play", "dvd", "blu_ray", "4k", "3d", "amz"]
        formats_split = formats.split(",")
        tv_movie = options["tv_movie"]

        tmdb_json = query_tmdb_by_imdb_id(imdb_id)
        tmdb_info = query_tmdb(imdb_id)

        if tv_movie:
            search_results = "tv_results"
            try:
                title = tmdb_json[search_results][0]["name"]
                year = tmdb_json[search_results][0]["first_air_date"].split("-")[0]
                poster = tmdb_json[search_results][0]["poster_path"]
                themoviedb_id = tmdb_json[search_results][0]["id"]
                genres = '[{"id": 10770, "name": "TV Movie"}]'
            except IndexError:
                print("No results for " + imdb_id)
                sys.exit(1)
        else:
            search_results = "movie_results"
            try:
                title = tmdb_json[search_results][0]["title"]
                year = tmdb_json[search_results][0]["release_date"].split("-")[0]
                poster = tmdb_json[search_results][0]["poster_path"]
                themoviedb_id = tmdb_json[search_results][0]["id"]
                genres = str(tmdb_info["genres"]).replace("\'", "\"")
            except IndexError:
                print("No results for " + imdb_id)
                sys.exit(1)

        # print(imdb_id)
        # print(formats)
        new_movie = Movie.objects.create(title=title,
                                         sort_title=title,
                                         primary_release_year=year,
                                         themoviedb_id=themoviedb_id,
                                         imdb_id=imdb_id,
                                         poster_path=poster,
                                         genres=genres)
        for f in formats_split:
            new_movie.formats.add(Format.objects.get(name=f))

        print("Movie '" + title + "' (" + str(year) + ") added")



