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
   
# class PlayListView(TemplateView):
#     template_name = 'chart/playlists.html'

#     # def get_context_data(self, **kwargs):
#     #     pl_cache = self.request.user.username + '_playlist_tracks'
#     #     user_playlists = cache.get(pl_cache)

#     #     print(pl_cache)
#     #     print(type(user_playlists))

#     #     if not user_playlists:
#     #         user_playlists = []

#     #         playlist_api_response = requests.get("https://api.spotify.com/v1/me/playlists",
#     #                                         headers=api_auth(self.request.user))
#     #         playlist_api_items = playlist_api_response.json()['items']
#     #         #print(playlist_api_items)

#     #         # Playlist Doc : https://developer.spotify.com/documentation/web-api/reference/playlists/get-a-list-of-current-users-playlists/
#     #         for playlist in playlist_api_items:
#     #             playlist = {'pl_name': playlist['name'],
#     #                         'pl_id': playlist['id'],
#     #                         'pl_tracks': playlist['tracks']['href'],
#     #                         'pl_track_count': playlist['tracks']['total']} # {href: full details of the tracks, total: total number of tracks}

#     #             tracks_query = {'fields':'items(track(name,href,album(name,href),artists,popularity))'}

#     #             if playlist['pl_track_count'] <= 100:
#     #                 playlist_tracks = cache.get_or_set(playlist['pl_tracks'],
#     #                                                     requests.get(playlist['pl_tracks'],
#     #                                                                 headers=api_auth(self.request.user),
#     #                                                                 params=tracks_query).json()['items'])

#     #             else:
#     #                 offset = 0
#     #                 playlist_tracks = []
#     #                 while offset <= playlist['pl_track_count']:
#     #                     tracks_query['offset'] = offset
#     #                     tracks_buffer = requests.get(playlist['pl_tracks'],
#     #                                                     headers=api_auth(self.request.user),
#     #                                                     params=tracks_query).json()['items']
#     #                     playlist_tracks.append(tracks_buffer)
#     #                     offset += 100
#     #             playlist['pl_tracks'] = playlist_tracks
#     #             user_playlists.append(playlist)

#     #         cache.set(pl_cache, user_playlists, None)

#     #     context = super(PlayListView, self).get_context_data(**kwargs)
#     #     context["playlists"] = user_playlists

#     #     # print(user_playlists)
        
#     #     return context

# #################################################### 
   
# ## if you don't want to user rest_framework 
   
# # def get_data(request, *args, **kwargs): 
# # 
# # data ={ 
# #             "sales" : 100, 
# #             "person": 10000, 
# #     } 
# # 
# # return JsonResponse(data) # http response 
   
   
# ####################################################### 
   
# ## using rest_framework classes 
   
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
