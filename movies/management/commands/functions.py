import requests

from movies.models import *


def query_tmdb_by_imdb_id(imdb_id):
    api_user = APIUser.objects.get(name="Leo")

    url = (
        f"https://api.themoviedb.org/3/find/{str(imdb_id)}"
        f"?api_key={api_user.api_key}&language=en-US&external_source=imdb_id"
    )

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def get_imdb_id_from_xml(id, root_discs):
    for disc in root_discs.iter("DiscTitle"):
        disc_id = disc.find(".")[1].text
        if disc_id == id:
            return disc.find(".")[11].text


def get_imdb_id(themoviedb_id):
    api_user = APIUser.objects.get(name="Leo")
    url = f"https://api.themoviedb.org/3/movie/{str(themoviedb_id)}?api_key={api_user.api_key}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    r_json = response.json()

    return r_json["imdb_id"]


def search_tmdb(title, year):
    api_user = APIUser.objects.get(name="Leo")
    url = (
        f"https://api.themoviedb.org/3/search/movie"
        f"?api_key={api_user.api_key}&language=en-US"
        f"&query={title}&page=1&include_adult=false&primary_release_year={str(year)}"
    )

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def query_tmdb(tmdb_id):
    api_user = APIUser.objects.get(name="Leo")

    url = f"https://api.themoviedb.org/3/movie/{str(tmdb_id)}?api_key={api_user.api_key}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()
