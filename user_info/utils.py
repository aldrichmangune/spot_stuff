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