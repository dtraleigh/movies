from django.contrib import admin
from django.urls import path

from movies import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("4k/", views.filter_4k, name="filter_4k"),
    path("BD/", views.filter_bd, name="filter_bd"),
    path("streaming/", views.filter_streaming, name="filter_streaming"),
    path("plex/", views.filter_plex, name="filter_plex"),
    path("genres/", views.genres, name="genres"),
    path("years/", views.years, name="years"),
]
