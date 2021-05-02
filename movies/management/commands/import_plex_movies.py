import xml.etree.ElementTree as ET
import requests

from django.core.management.base import BaseCommand

from movies.models import *
from movies.management.commands.functions import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open("plex_list.txt") as f:
            for line in f:
                title = line[:line.find(" (")]
                year = line[line.find("(") + 1: line.find(")")]
                tmdb_search = search_tmdb(title, year)

                try:
                    # If search returns just one result, go with it
                    if tmdb_search["total_results"] == 1:
                        tmdb_result = tmdb_search["results"][0]
                        themoviedb_id = tmdb_result["id"]
                        poster = tmdb_result["poster_path"]
                        imdb_id = get_imdb_id_from_xml(themoviedb_id)

                        new_movie = Movie.objects.create(title=title,
                                                         sort_title=title,
                                                         primary_release_year=year,
                                                         themoviedb_id=themoviedb_id,
                                                         imdb_id=imdb_id,
                                                         poster_path=poster,
                                                         )
                        new_movie.formats.add(Format.objects.get(name="plex"))
                        print("1 result for " + title + ". Adding movie.")
                    elif tmdb_search["total_results"] > 1:
                        # Pick the one with a higher vote_count
                        tmdb_results = tmdb_search["results"]

                        vote_count = 0
                        for result1 in tmdb_results:
                            if result1["vote_count"] > vote_count:
                                vote_count = result1["vote_count"]

                        for result2 in tmdb_results:
                            if result2["vote_count"] == vote_count:
                                result_title = result2["title"]
                                themoviedb_id = result2["id"]
                                poster = result2["poster_path"]
                                imdb_id = get_imdb_id_from_xml(themoviedb_id)
                                new_movie = Movie.objects.create(title=title,
                                                                 sort_title=title,
                                                                 primary_release_year=year,
                                                                 themoviedb_id=themoviedb_id,
                                                                 imdb_id=imdb_id,
                                                                 poster_path=poster,
                                                                 )
                                new_movie.formats.add(Format.objects.get(name="plex"))
                                break

                        print(str(len(tmdb_results)) + " results for " + title + ". Adding " + result_title)
                    else:
                        print("*************No results for " + title)
                except:
                    print("<<<<<<<<< Investigate " + title)
