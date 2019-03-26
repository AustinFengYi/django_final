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
from .models import Singer,Category,Album
from django.shortcuts import render, get_object_or_404


from itertools import chain

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
  return render(request,'music/album_rank.html')
  
def music_news(request):
  return render(request,'music/music_news.html')

def list_of_album_by_category(request, category_id):
  categories = Category.objects.all()
  if category_id:
    category = get_object_or_404(Category,pk=category_id)
    albums = Album.objects.filter(category=category)
    singers = Singer.objects.filter(category=category)
  template_name = 'music/category/list_of_album_by_category.html'
  context = {'categories':categories,'albums':albums,'singers':singers ,'category':category}
  return render(request, template_name, context)

# singer/show
def singer_show(request, singer_id):
  singer = get_object_or_404(Singer,pk=singer_id)
  return render(request, 'music/singer_show.html',{'singer':singer})

class DetailView(generic.DetailView):
  model = Album
  template_name = 'music/detail.html'


class AlbumCreate(CreateView):
  model = Album
  fields = ['artist','album_title','genre','album_logo']


class AlbumUpdate(UpdateView):
  model = Album
  fields = ['artist','album_title','genre','album_logo']

class AlbumDelete(DeleteView):
  model = Album
  success_url = reverse_lazy('music:index')







