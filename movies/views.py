from django.db.models import Q
from django.shortcuts import render
from django.db.models import Max

import random

from movies.management.commands.functions import *
from movies.models import *
from movies.functions import *


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


def home(request):
    search = request.GET.get("search")
    sort = request.GET.get("sort")
    movie_list, search, sort, sort_arrow = get_movies(search, sort, None, "sort_title")
    breadcrumb = str(len(movie_list)) + " Titles"
    sort_label = "Alphabetical"
    movie_recent_list = Movie.objects.order_by("-created_date")[0:12]

    return render(request, "home.html", {"movie_list": movie_list,
                                         "search": search,
                                         "breadcrumb": breadcrumb,
                                         "sort": sort,
                                         "sort_arrow": sort_arrow,
                                         "sort_label": sort_label,
                                         "movie_recent_list": movie_recent_list})


def filter_4k(request):
    sort = request.GET.get("sort")
    uhd_movies, search, sort, sort_arrow = get_movies(None, sort, "4k", "sort_title")
    breadcrumb = "4K Titles (" + str(len(uhd_movies)) + ")"
    sort_label = "Alphabetical"

    return render(request, "movie_grid.html", {"movie_list": uhd_movies,
                                               "breadcrumb": breadcrumb,
                                               "sort": sort,
                                               "sort_arrow": sort_arrow,
                                               "sort_label": sort_label})


def filter_bd(request):
    sort = request.GET.get("sort")
    bd_movies, search, sort, sort_arrow = get_movies(None, sort, "blu_ray", "sort_title")
    breadcrumb = "Blu-Ray Titles (" + str(len(bd_movies)) + ")"
    sort_label = "Alphabetical"

    return render(request, "movie_grid.html", {"movie_list": bd_movies,
                                               "breadcrumb": breadcrumb,
                                               "sort": sort,
                                               "sort_arrow": sort_arrow,
                                               "sort_label": sort_label})


def filter_streaming(request):
    streaming_movies = Movie.objects.filter(
        Q(formats__name="amz") |
        Q(formats__name="vudu") |
        Q(formats__name="ma") |
        Q(formats__name="apple_tv") |
        Q(formats__name="g_play")).distinct().order_by("sort_title")
    breadcrumb = "Streaming Titles (" + str(len(streaming_movies)) + ")"
    sort_label = "Alphabetical"

    return render(request, "movie_grid.html", {"movie_list": streaming_movies,
                                               "breadcrumb": breadcrumb,
                                               "sort_label": sort_label})


def filter_plex(request):
    sort = request.GET.get("sort")
    plex_movies, search, sort, sort_arrow = get_movies(None, sort, "plex", "sort_title")
    breadcrumb = "Titles on Plex (" + str(len(plex_movies)) + ")"
    sort_label = "Alphabetical"

    return render(request, "movie_grid.html", {"movie_list": plex_movies,
                                               "breadcrumb": breadcrumb,
                                               "sort": sort,
                                               "sort_arrow": sort_arrow,
                                               "sort_label": sort_label})


def genres(request):
    movie_list = Movie.objects.all().order_by("sort_title")
    breadcrumb = "Titles sorted by Genre"
    sort_label = "Alphabetical"

    # ["Action", "Romance", ...]
    all_genres = []
    for movie in movie_list:
        genre_list = json.loads(movie.genres)
        for g in genre_list:
            all_genres.append(g["name"])
    all_genres = list(set(all_genres))

    # [["Genre 1", Movie A], ["Genre 2", Movie A] ...]
    movie_list_w_genres = []

    for movie in movie_list:
        genre_list = json.loads(movie.genres)
        for g in genre_list:
            movie_list_w_genres.append([g["name"], movie])

    all_genres.sort()

    return render(request, "genres.html", {"movie_list": movie_list_w_genres,
                                           "all_genres": all_genres,
                                           "breadcrumb": breadcrumb,
                                           "sort_label": sort_label})


def years(request):
    sort = request.GET.get("sort")
    breadcrumb = "Titles sorted by Year"
    sort_label = "Release Year"
    movie_list, search, sort, sort_arrow = get_movies(None, sort, None, "primary_release_year")

    return render(request, "movie_grid.html", {"movie_list": movie_list,
                                               "breadcrumb": breadcrumb,
                                               "sort": sort,
                                               "sort_arrow": sort_arrow,
                                               "sort_label": sort_label})


def rand_movie(request):
    sort = request.GET.get("sort")
    movie_list = [get_random_movie()]
    breadcrumb = ""
    sort_label = "Alphabetical"

    return render(request, "movie_grid.html", {"movie_list": movie_list,
                                               "breadcrumb": breadcrumb,
                                               "sort": sort,
                                               "sort_label": sort_label})


def ind_movie(request, tmdb_id):
    movie_info = query_tmdb(tmdb_id)
    movie = Movie.objects.get(themoviedb_id=tmdb_id)

    if movie.letterboxd_url_slug:
        letterboxd_page = get_page_content(f"https://letterboxd.com/film/{movie.letterboxd_url_slug}")
        letterboxd_page_soup = BeautifulSoup(letterboxd_page.content, "html.parser")
        letterboxd_page_avg_rating = get_letterboxd_page_avg_rating(letterboxd_page_soup)
    else:
        letterboxd_page_avg_rating = None

    try:
        if movie_info["id"]:
            title = movie_info["title"]
            year = movie_info["release_date"][:4]
            tagline = movie_info["tagline"]
            poster_path = movie_info["poster_path"]
            overview = movie_info["overview"]
            runtime = str(movie_info["runtime"])
            genres_list = [g["name"] for g in movie_info["genres"]]
    except KeyError:
        title = movie.title
        year = movie.primary_release_year
        tagline = None
        poster_path = movie.poster_path
        overview = None
        runtime = None
        genres_list = genres

    return render(request, "movie.html", {"tmdb_id": tmdb_id,
                                          "title": title,
                                          "year": year,
                                          "tagline": tagline,
                                          "poster_path": poster_path,
                                          "overview": overview,
                                          "runtime": runtime,
                                          "movie": movie,
                                          "genres_list": genres_list,
                                          "rating": letterboxd_page_avg_rating})
