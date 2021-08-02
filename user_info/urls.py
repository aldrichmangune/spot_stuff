from django.urls import path, include

from . import views
from .views import UserLogin, home
app_name = 'user_info'

urlpatterns = [
    path('login',UserLogin,name='login'),
    path('', home,name='home'),
    path('chart/', include('chart.urls')),
    path('playlists/', views.PlayListView.as_view(), name='playlists'),
]
