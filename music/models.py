from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Singer(models.Model):
  category = models.ForeignKey("Category")
  singer_name = models.CharField(max_length = 50)
  singer_intro = models.CharField(max_length = 1000,blank=True)
  singer_avatar = models.FileField(blank=True)
  is_favorite = models.BooleanField(default=False,blank=True)

  def __str__(self):
    return self.singer_name + ' - ' + self.singer_intro

class Category(models.Model):
  name = models.CharField(max_length = 50)
  
  def __str__(self):
    return self.name

  #def get_absoulte_url(self):
    #return reverse('music:list_of_album_by_category', kwargs={'pk':self.pk})

class Album(models.Model):
  category = models.ForeignKey(Category)
  singer = models.ForeignKey(Singer)
  album_title = models.CharField(max_length = 500)
  album_logo = models.FileField()
  album_intro = models.CharField(max_length = 1000)
  album_release_date = models.CharField(max_length = 30)


  genre = models.CharField(max_length = 100,blank=True)
  artist = models.CharField(max_length = 250,blank=True)

  def get_absoulte_url(self):
    return reverse('music:detail', kwargs={'pk':self.pk})

  def __str__(self):
    return self.album_title + ' - ' + self.album_release_date + ' - ' + self.album_intro

class Song(models.Model):
  #singer = models.ForeignKey(Singer)
  category = models.ForeignKey(Category)
  album = models.ForeignKey(Album, on_delete=models.CASCADE)
  song_name = models.CharField(max_length = 100)
  song_lyric = models.CharField(max_length = 1000,blank=True)
  audio_file = models.FileField()
 

  def __str__(self):
    return self.song_name + ' - ' + self.song_lyric


class Youtube(models.Model):
  website = models.CharField(max_length=500)
  song_name = models.CharField(max_length=80)

  def __str__(self):
    return self.website + '-' + self.song_name



