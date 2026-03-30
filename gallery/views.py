from django.shortcuts import render, get_object_or_404
from .models import PhotoAlbum

def gallery_list(request):
    """Сторінка з усіма альбомами"""
    albums = PhotoAlbum.objects.all()
    return render(request, 'gallery/gallery_list.html', {'albums': albums})

def album_detail(request, pk):
    """Сторінка конкретного альбому з фото"""
    album = get_object_or_404(PhotoAlbum, pk=pk)
    return render(request, 'gallery/album_detail.html', {'album': album})