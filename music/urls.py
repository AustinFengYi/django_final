from django.conf.urls import url
from .import views

app_name = 'music'



urlpatterns = [
    #default hamepage
    # /music/
    url(r'^$',views.IndexView.as_view(),name = 'index'),

    # /music/712/
    url(r'^(?P<pk>[0-9]+)/$',views.DetailView.as_view(), name='detail' ),

    # /music/category/album
    url(r'^category/(?P<category_id>[0-9]+)/$', views.list_of_album_by_category, name='list_of_album_by_category'),

    # /music/album/add/
    url(r'album/add/$',views.AlbumCreate.as_view(), name='album-add'),

    # /music/album/edit/
    url(r'album/(?P<pk>[0-9]+)/$',views.AlbumUpdate.as_view(), name='album-update'),

    # /music/album/2/delete/
    url(r'album/(?P<pk>[0-9]+)/$',views.AlbumDelete.as_view(), name='album-delete'),

    # /music/singer_show/
    url(r'^singer_show/(?P<singer_id>[0-9]+)/$',views.singer_show, name='singer_show' ),

    # /music/singer_profile/
    url(r'^singer_profile/(?P<singer_id>[0-9]+)/$',views.singer_profile, name='singer_profile' ),

    # /music/album_rank/
    url(r'^album_rank/$',views.album_rank, name='album_rank' ),

    # /music/music_mood/
    url(r'^music_mood/$',views.music_mood, name='music_mood' ),

    # /music/music_critic/
    url(r'^music_critic/$',views.music_critic, name='music_critic' ),

     # /music/favorite/
    #url(r'^(?P<album_id>[0-9]+)/favorite/$',views.favorite, name='favorite' ),
]

