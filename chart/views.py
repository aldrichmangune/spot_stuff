from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.core.cache import cache
from django.contrib.auth import get_user_model

from rest_framework.views import APIView 
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response 

from .utils import api_auth, get_artist_genres

import requests
import json
import random

user = get_user_model()

# Create your views here.
class HomeView(View): 
    def get(self, request, *args, **kwargs): 
        return render(request, 'chart/index.html')

class PlaylistChartView(TemplateView):
    template_name = 'chart/playlist_chart.html'
    slug_url_kwarg = 'playlist_id'

class GenreView(TemplateView): 
    template_name = 'chart/genre.html'
    print(user.username)
    # genre_artists = cache.get(str(user.username) + '_playlist_tracks')
    # print(genre_artists)
   
class ChartData(APIView): 
    authentication_classes = [SessionAuthentication, BasicAuthentication] 
    permission_classes = [] 
   
    # def get_queryset(self):
    #     playlist_id = self.request.query_params.get('playlist_id')
    #     return super().get_queryset()

    def get(self, request, format = None): 
        playlist_id = request.GET.get('playlist_id', '')
        pl_cache = str(request.user) + '_playlist_tracks'
        playlists = cache.get(pl_cache)
        for playlist in playlists:
            if playlist_id == playlist['pl_id']:
                target_p = playlist
        # print(target_p)

        artist_ids = []
        
        for track in target_p['pl_tracks']:
            # print(track['track'])
            for artist in track['track']['artists']:
                # print(artist['id'])
                artist_ids.append(artist['id'])

        artist_genre_list = cache.get(target_p['pl_id'] + '_genres')

        if not artist_genre_list:
            artist_genre_list = get_artist_genres(target_p['pl_id'], artist_ids, request.user)
            cache.set(target_p['pl_id'] + '_genres', artist_genre_list)
        else:
            print('found cached')

        genre_count = {}
        for artist_genre in artist_genre_list:
            # print(artist_genre)
            # if 'modern rock' in artist_genre['genres']:
            #     print(artist_genre)
            for genre in artist_genre['genres']:
                if not genre in genre_count:
                    genre_count[genre] = 1
                else:
                    genre_count[genre] += 1
        # print(sorted(genre_count.items(), key=lambda x: x[1], reverse=True))
        labels = [] 
        chartdata = [] 
        chartLabel = target_p['pl_name']

        colors = []
        for genre, count in genre_count.items():
            labels.append(genre)
            chartdata.append(count)
            r = lambda: random.randint(0,255)
            color = '#{:02x}{:02x}{:02x}'.format(r(),r(),r())
            colors.append(color)
            # print('#%02X%02X%02X' % (r(),r(),r()))
            

        data = { 
                    "labels":labels, 
                    "chartLabel":chartLabel, 
                    "chartdata":chartdata,
                    "backgroundColor": colors,
                } 
        return Response(data) 