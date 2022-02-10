import requests
import json
from bs4 import BeautifulSoup
import random

from movies.models import Movie
from django.db.models import Max


def get_page_content(link):
    try:
        response = requests.get(link, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Connection problem to {link}")
        print(e)
        response = None

    return response


def get_letterboxd_page_movie_title(s):
    try:
        return s.find("h1", {"class": "headline-1 js-widont prettify"}).get_text()
    except AttributeError:
        print("Couldn't find a movie_title")
        print(s.find("h1", {"class": "headline-1 js-widont prettify"}))
        return None


def get_letterboxd_page_movie_year(s):
    letterboxd_page_movie_year = None
    letterboxd_page_links = s.find_all("a")
    for link in letterboxd_page_links:
        try:
            if "/films/year/" in link["href"]:
                letterboxd_page_movie_year = link.get_text()
        except KeyError:
            pass
    return letterboxd_page_movie_year


def get_letterboxd_page_avg_rating(s):
    rating = None
    CDATA_script = None
    scripts = s.find_all("script")

    for script in scripts:
        if "CDATA" in str(script):
            CDATA_script = str(script)
    try:
        json_str = CDATA_script.split("/*")[1].split("*/")[1]
        movie_json = json.loads(json_str)
        rating = movie_json["aggregateRating"]["ratingValue"]
        return round(rating, 1)
    except TypeError as e:
        print(e)
        return rating


def get_sort_character(sort_order):
    if sort_order == "desc":
        return "⌄"
    return "⌃"


def get_movies(search, sort, movie_format_filter, order_by):
    """Sort"""
    if sort == "desc":
        sort = "asc"
        order_by = "-" + order_by
        sort_arrow = get_sort_character("desc")
    else:
        sort = "desc"
        sort_arrow = get_sort_character("asc")

    if search:
        if search.lower() == "3d":
            movie_list = Movie.objects.filter(formats__name="3d").order_by(order_by)
        else:
            movie_list = Movie.objects.filter(title__icontains=search).order_by(order_by)
    else:
        movie_list = Movie.objects.order_by(order_by)

    if movie_format_filter:
        movie_list = Movie.objects.filter(formats__name=movie_format_filter).order_by(order_by)

    return movie_list, search, sort, sort_arrow


def get_random_movie():
    max_id = Movie.objects.all().aggregate(max_id=Max("id"))["max_id"]
    while True:
        pk = random.randint(1, max_id)
        random_movie = Movie.objects.filter(pk=pk).first()
        if random_movie:
            return random_movie
