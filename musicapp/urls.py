from django.urls import path
from .views import AddArtiste, DeleteArtiste, GetAllArtistes, GetAllSongs, GetSingleSong, \
DeleteSong, AddLyrics, AddSongs, UpdateArtiste, GetAllLyrics


urlpatterns = [
    path('add-artiste/', AddArtiste.as_view(), name="Add Artistes"),
    path('delete-artiste/<int:artiste_id>/', DeleteArtiste.as_view(), name="Delete Artiste"),
    path('all-artistes/', GetAllArtistes.as_view(), name="Get All Artistes"),
    path('all-songs/', GetAllSongs.as_view(), name="Get All Songs"),
    path('all-lyrics/', GetAllLyrics.as_view(), name="Get All Lyrics"),
    path('single-song/<int:song_id>/', GetSingleSong.as_view(), name="Get Single Song"),
    path('delete-song/<int:song_id>/', DeleteSong.as_view(), name="Delete Song"),
    path('add-lyrics/<int:song_id>/', AddLyrics.as_view(), name="Add lyrics"),
    path('add-song/<int:artiste_id>/', AddSongs.as_view(), name="Add Songs"),
    path('update-artiste/<int:artiste_id>/', UpdateArtiste.as_view(), name="Update Artiste"),
]