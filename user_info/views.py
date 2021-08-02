from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.conf import settings

import requests
import json

# Create your views here.
def index(request):
    return render(request, 'index.html')

def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('playlists/')
    return render(request, 'user_info/index.html')

def UserLogin(request):
    return render(request, 'user_info/login.html')
    

def callback_view(request, *args, **kwargs):
    return render(request, "callback.html", {})

class PlayListView(TemplateView):
    template_name = 'user_info/playlists.html'

    # def get_context_data(self, **kwargs):
    #     pl_cache = self.request.user.username + '_playlist_tracks'
    #     user_playlists = cache.get(pl_cache)

    #     print(pl_cache)
    #     print(type(user_playlists))

    #     if not user_playlists:
    #         user_playlists = []

    #         playlist_api_response = requests.get("https://api.spotify.com/v1/me/playlists",
    #                                         headers=api_auth(self.request.user))
    #         playlist_api_items = playlist_api_response.json()['items']
    #         #print(playlist_api_items)

    #         # Playlist Doc : https://developer.spotify.com/documentation/web-api/reference/playlists/get-a-list-of-current-users-playlists/
    #         for playlist in playlist_api_items:
    #             playlist = {'pl_name': playlist['name'],
    #                         'pl_id': playlist['id'],
    #                         'pl_tracks': playlist['tracks']['href'],
    #                         'pl_track_count': playlist['tracks']['total']} # {href: full details of the tracks, total: total number of tracks}

    #             tracks_query = {'fields':'items(track(name,href,album(name,href),artists,popularity))'}

    #             if playlist['pl_track_count'] <= 100:
    #                 playlist_tracks = cache.get_or_set(playlist['pl_tracks'],
    #                                                     requests.get(playlist['pl_tracks'],
    #                                                                 headers=api_auth(self.request.user),
    #                                                                 params=tracks_query).json()['items'])

    #             else:
    #                 offset = 0
    #                 playlist_tracks = []
    #                 while offset <= playlist['pl_track_count']:
    #                     tracks_query['offset'] = offset
    #                     tracks_buffer = requests.get(playlist['pl_tracks'],
    #                                                     headers=api_auth(self.request.user),
    #                                                     params=tracks_query).json()['items']
    #                     playlist_tracks.append(tracks_buffer)
    #                     offset += 100
    #             playlist['pl_tracks'] = playlist_tracks
    #             user_playlists.append(playlist)

    #         cache.set(pl_cache, user_playlists, None)

    #     context = super(PlayListView, self).get_context_data(**kwargs)
    #     context["playlists"] = user_playlists

    #     # print(user_playlists)
        
    #     return context

#################################################### 
   
## if you don't want to user rest_framework 
   
# def get_data(request, *args, **kwargs): 
# 
# data ={ 
#             "sales" : 100, 
#             "person": 10000, 
#     } 
# 
# return JsonResponse(data) # http response 
   
   
####################################################### 
   
## using rest_framework classes 