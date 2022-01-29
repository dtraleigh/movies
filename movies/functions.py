import requests
import json
from bs4 import BeautifulSoup


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
