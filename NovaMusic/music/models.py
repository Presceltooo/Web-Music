from django.db import models
from django.contrib.auth import get_user_model
from core.models import Comment
from artist.models import Artist
from genre.models import Genre
from album.models import Album

class Music(models.Model):
    '''Music model'''
    class Meta:
        verbose_name = 'Music'
        verbose_name_plural = 'Music'

    title = models.CharField(max_length=220)
    thumbnail = models.ImageField(upload_to='SongsThumbnails/', default='SongsThumbnails/default.jpg')
    artists = models.ManyToManyField(Artist)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    song = models.FileField(upload_to='Songs/', null=True, blank=True)
    song_duration = models.CharField(max_length=200, null=True, blank=True)
    lyrics = models.TextField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    published = models.BooleanField(default=False)
    page_view = models.IntegerField(default=0)
    single_track = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    audio_url = models.URLField(max_length=500, blank=True, null=True, help_text="Link mp3 hoặc stream nhạc")
    audio_file = models.FileField(upload_to='music/', blank=True, null=True, help_text="File mp3 thực tế (nếu có)")

    def get_album_name(self):
        '''If the music object is connected to a album then get album name'''
        try:
            return self.album.title
        except:
            pass

    def __str__(self):
        return self.title


class MusicComment(Comment):
    '''Music comment model inherit from main Comment model'''
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    
    def comment_title(self):
        return f'Comment on {self.music} by {self.owner.name if self.owner.name else self.owner.email}'

class Playlist(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='playlists')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='songs')
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.music.title} in {self.playlist.title}"

class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE, null=True, blank=True)
    album = models.ForeignKey('album.Album', on_delete=models.CASCADE, null=True, blank=True)
    artist = models.ForeignKey('artist.Artist', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.user.email}"