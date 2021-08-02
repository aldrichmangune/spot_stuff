from django.contrib import admin 
from django.urls import path
from . import views

app_name='chart'
  
urlpatterns = [ 
    path('', views.HomeView.as_view()), 
    # path('test-api', views.get_data), 
    path('api/', views.ChartData.as_view()),
    # path('playlists/', views.PlayListView.as_view(), name='playlists'),
    path('<slug:playlist_id>', views.PlaylistChartView.as_view(), name='playlist_chart')
] 