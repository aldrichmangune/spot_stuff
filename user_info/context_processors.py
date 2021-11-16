from django.core.cache import cache

from .utils import api_auth

import requests

def playlists(request):
    pl_cache = request.user.username + '_playlist_tracks'
    # cache.clear()
    user_playlists = cache.get(pl_cache)

    # print(pl_cache)
    # print(type(user_playlists))
    if (request.user.id):
        if not user_playlists:
            user_playlists = []
            

            playlist_api_response = requests.get("https://api.spotify.com/v1/me/playlists",
                                            headers=api_auth(request.user),
                                            params={'limit':50})
            playlist_api_items = playlist_api_response.json()['items']
            #print(playlist_api_items)

            # Playlist Doc : https://developer.spotify.com/documentation/web-api/reference/playlists/get-a-list-of-current-users-playlists/
            for playlist in playlist_api_items:
                playlist = {'pl_name': playlist['name'],
                            'pl_id': playlist['id'],
                            'pl_owner': playlist['owner']['display_name'],
                            'pl_tracks': playlist['tracks']['href'],
                            'pl_track_count': playlist['tracks']['total']} # {href: full details of the tracks, total: total number of tracks}

                tracks_query = {'fields':'items(track(id,name,album(name,id),artists(name,id),popularity))'}

                if playlist['pl_track_count'] <= 100:
                    playlist_tracks = cache.get_or_set(playlist['pl_tracks'],
                                                        requests.get(playlist['pl_tracks'],
                                                                    headers=api_auth(request.user),
                                                                    params=tracks_query).json()['items'])

                else:
                    offset = 0
                    playlist_tracks = []
                    while offset <= playlist['pl_track_count']:
                        tracks_query['offset'] = offset
                        tracks_buffer = requests.get(playlist['pl_tracks'],
                                                        headers=api_auth(request.user),
                                                        params=tracks_query).json()['items']
                        playlist_tracks.extend(tracks_buffer)
                        offset += 100
                playlist['pl_tracks'] = playlist_tracks
                user_playlists.append(playlist)

            cache.set(pl_cache, user_playlists, None)

        # context = super(PlayListView, self).get_context_data(**kwargs)
        # context["playlists"] = user_playlists

        # print(user_playlists)
        
        return {'playlists':user_playlists}
    return {}

# def genres(request):
