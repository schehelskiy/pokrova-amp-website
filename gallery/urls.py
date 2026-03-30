from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery_list, name='gallery_list'),
    path('album/<int:pk>/', views.album_detail, name='album_detail'),
]