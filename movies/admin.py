from django.contrib import admin
from movies.models import *


class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "primary_release_year", "get_formats",
                    "themoviedb_id", "imdb_id", "sort_title", "modified_date")


class FormatAdmin(admin.ModelAdmin):
    list_display = ("name",)


class APIUserAdmin(admin.ModelAdmin):
    list_display = ("name", "api_key")


class CollectionAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


admin.site.register(Movie, MovieAdmin)
admin.site.register(Format, FormatAdmin)
admin.site.register(APIUser, APIUserAdmin)
admin.site.register(Collection, CollectionAdmin)
