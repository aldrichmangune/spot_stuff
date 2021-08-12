from django.core.cache import cache

from .utils import api_auth

import requests

def genre_artists(request):
    genre_artists = cache.get(request.user.username + '_playlist_tracks')
    return {'genre_artists':genre_artists}
