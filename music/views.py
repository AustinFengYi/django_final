# Create your views here.
"""
from django.shortcuts import render, get_object_or_404
from .models import Album,Song

def index(request):
  all_albums = Album.objects.all()
  return render(request,'music/index.html', {'all_albums':all_albums})

def detail(request, album_id):
  #album = Album.objects.get(id = album_id)
  album = get_object_or_404(Album,pk=album_id)
  return render(request, 'music/detail.html',{'album':album})

def favorite(request,album_id):
  album = get_object_or_404(Album,pk=album_id)
  try:
    selected_song = album.song_set.get(pk=request.POST['song'])
  except(KeyError, Song.DoesNotExist):
    return render(request,'music/detail.html', {'album':album, 'error_message':"這不是有效的歌曲",})
  else:
    selected_song.favorite = True
    selected_song.save()
    return render(request, 'music/detail.html',{'album':album})
"""

from django.views import generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Singer,Category,Album,Youtube,Song,Critic
from django.shortcuts import render, get_object_or_404


from itertools import chain
import requests
import random
from bs4 import BeautifulSoup
from django.http import HttpResponse

from django import forms

class IndexView(generic.ListView):
  template_name = 'music/index.html'
  #context_object_name = 'all_albums'
   
  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super().get_context_data(**kwargs)
    # Add in a QuerySet of all the books
    context['all_albums'] = Album.objects.all()
    context['all_categories'] = Category.objects.all()
    context['all_singers'] = Singer.objects.all()
    return context


  def get_queryset(self):
    all_albums = Album.objects.all()
    all_categories = Category.objects.all()
    all_singers = Singer.objects.all()
    return chain(all_albums, all_categories, all_singers)

def album_rank(request):
  all_albums = Album.objects.all()

  return render(request,'music/album_rank.html',{'all_albums':all_albums})


def music_mood(request):
  #刪除前一次操作 save 的資料
  Youtube.objects.all().delete()

  # 需要選擇心情後才開始執行爬蟲選歌
  if request.method == 'POST':
    # 選擇心情
    if 'high' in request.POST:
      url = "https://www.youtube.com/playlist?list=PLtAw-mgfCzRydST1D3nER8Sp-dLLM4mbT"
    if 'emotion' in request.POST:
      url = "https://www.youtube.com/playlist?list=PLA3DA2BBAAD48990D"
    if 'happy' in request.POST:
      url = "https://www.youtube.com/playlist?list=PLsyOSbh5bs16vubvKePAQ1x3PhKavfBIl"
    html = requests.get(url)
    #content = request.content
    soup = BeautifulSoup(html.text, "html.parser")
    for all_mv in soup.select(".pl-video-title"):
      data = all_mv.select("a")
      song_name = data[0].get_text()
      #Youtube.objects.create(song_name = song_name)
      #print("https://www.youtube.com{}".format(data[0].get("href").split('&')[0]))
      html_text = "https://www.youtube.com{}".format(data[0].get("href").split('&')[0])
      HttpResponse(Youtube.objects.create(website= html_text,song_name = song_name))
    youtube =  Youtube.objects.all()

    # list the order
    random_youtube = list(youtube)
    # random the order
    random.shuffle(random_youtube)
    # get the first video, take embed IDcode of Youtube
    str1 = ''.join(map(str,random_youtube)).split('v=')[1][0:11]

    # get the first video after random order
    one_youtube  = random_youtube[0]

    context = { 'youtube':youtube, 'one_youtube':one_youtube, 'str1':str1 }
    return render(request,'music/music_mood.html',context)
  else:
    return render(request,'music/music_mood.html')



def music_critic(request):
  #刪除前一次操作 save 的資料
  Critic.objects.all().delete()

  # 需要選擇類型後才開始執行爬蟲
  if request.method == 'POST':
    # 選擇類型
    if 'chinese' in request.POST:
      url = "https://www.playmusic.tw/music_critics.php"
    if 'japan_korea' in request.POST:
      url = "https://www.playmusic.tw/music_critics.php?type=JK&selected=2"
    if 'western' in request.POST:
      url = "https://www.playmusic.tw/music_critics.php?type=Western&selected=1"
    
    html = requests.get(url)
    #content = request.content
    soup = BeautifulSoup(html.text, "html.parser")



    for all_news in soup.select(".article_index"):
        data_image = all_news.select("img")
        html_image = "https://www.playmusic.tw/{}".format(data_image[0].get("src"))
        
        data = all_news.select(".text")
        html_title = data[0].get_text()
        
        data_a = all_news.select("a")
        html_website = "https://www.playmusic.tw/{}".format(data_a[0].get("href"))
        
        
        data_date = all_news.select(".indent-top1")
        html_date = data_date[0].get_text()

        HttpResponse(Critic.objects.create(image_website= html_image,name = html_title, time = html_date, link_website = html_website))

    critic =  Critic.objects.all()


    context = { 'critic':critic }
    return render(request,'music/music_critic.html',context)
  else:
    return render(request,'music/music_critic.html')
  

def list_of_album_by_category(request, category_id):
  categories = Category.objects.all()
  if category_id:
    category = get_object_or_404(Category,pk=category_id)
    albums = Album.objects.filter(category=category)
    singers = Singer.objects.filter(category=category)
    songs = Song.objects.filter(category=category)
  template_name = 'music/category/list_of_album_by_category.html'
  context = {'categories':categories,'albums':albums,'singers':singers ,'category':category,'songs':songs}
  return render(request, template_name, context)

# singer/show
def singer_show(request, singer_id):
  singer = get_object_or_404(Singer,pk=singer_id)
  return render(request, 'music/singer_show.html',{'singer':singer})

# singer/profile
def singer_profile(request, singer_id):
  singer = get_object_or_404(Singer,pk=singer_id)
  return render(request, 'music/singer_profile.html',{'singer':singer})

class DetailView(generic.DetailView):
  model = Album
  template_name = 'music/detail.html'

  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super().get_context_data(**kwargs)
    # Add in a QuerySet of all the books
    
    context['other_albums'] = Album.objects.all()
    return context


class AlbumCreate(CreateView):
  model = Album
  fields = ['artist','album_title','genre','album_logo']


class AlbumUpdate(UpdateView):
  model = Album
  fields = ['artist','album_title','genre','album_logo']

class AlbumDelete(DeleteView):
  model = Album
  success_url = reverse_lazy('music:index')







