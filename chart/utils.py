from django.utils import timezone
from social_django.utils import load_strategy

import datetime
import requests

def api_auth(user):
    social = user.social_auth.get(provider='spotify')
    time_diff = timezone.now().replace(tzinfo=None) - datetime.datetime.utcfromtimestamp(social.extra_data['auth_time'])
    # print(time_diff.total_seconds())
    if time_diff.total_seconds() >= 3600:
        print("auth expired")
        social.refresh_token(load_strategy())
    access_token = social.get_access_token(load_strategy())
    return {'Authorization':'Bearer ' + access_token}

def get_multiple_track_features(ids):
    print(ids)
    # playlist_api_response = requests.get("https://api.spotify.com/v1/me/playlists",
    #                                     headers=api_auth(request.user))
    pass

def get_artist_genres(pl_id, ids, user):
    buffer_index = 0
    genres = []


    # Call API with buffers to get all artist information
    response_full = []
    for buffer_index in range(0, len(ids), 50):
        last_index = min(buffer_index + 50, len(ids))
        # print('Num of ids:', len(ids))
        batch = ids[buffer_index:last_index]
        # print(ids[buffer_index:last_index])
        # print('Querying: {} - {}'.format(buffer_index, last_index))
        query_ids = {'ids': ','.join(filter(None, batch))}
        # print('--- BATCH --- {} - {}: {}'.format(buffer_index,last_index,len(ids[buffer_index:last_index])))
        # print(query_ids)
        response_artists = requests.get("https://api.spotify.com/v1/artists",
                                        headers=api_auth(user),
                                        params=query_ids).json()['artists']
        # print(response_artists)
        response_full.extend(response_artists)

    # print(response_full)
    # Trim response to artist id, name, and genres and add to full list
    for artist in response_full:
        # print(artist)
        id_artist_genre = {'id': artist['id'],
                            'name': artist['name'],
                            'genres': artist['genres']}
        genres.append(id_artist_genre)

    # for genre in genres:
    #     print(genre)

    return genres