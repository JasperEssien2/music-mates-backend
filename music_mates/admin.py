from django.contrib import admin

from . import models


class ArtistInlineModel(admin.TabularInline):
    model = models.Artist

@admin.register(models.Artist)
class ArtistAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'image_url',
        'description'
    ]


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'image_url',
        'google_id',
        'favourite_artists'
    ]

    list_display = [
        'name',
        'image_url',
        'google_id',
    ]

