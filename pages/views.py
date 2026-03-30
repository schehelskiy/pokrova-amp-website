from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Імпорти твоїх моделей
from news.models import Post
from team.models import Player
from matches.models import Match
from .models import FanPhoto
from .forms import FanRegistrationForm


def home(request):
    """Головна сторінка: показує матчі та новини (Слайдер)"""
    now = timezone.now()

    # === НОВА ЛОГІКА ДЛЯ МАТЧІВ (ОСНОВНА КОМАНДА) ===
    upcoming_main = Match.objects.filter(team_type='MAIN', date__gte=now).order_by('date')
    # Беру 5 останніх, щоб на телефоні можна було гарно їх скролити пальцем
    past_main = Match.objects.filter(team_type='MAIN', date__lt=now, is_finished=True).order_by('-date')[:5]

    # === НОВА ЛОГІКА ДЛЯ МАТЧІВ (ПОКРОВА 2) ===
    upcoming_second = Match.objects.filter(team_type='SECOND', date__gte=now).order_by('date')
    past_second = Match.objects.filter(team_type='SECOND', date__lt=now, is_finished=True).order_by('-date')[:5]

    # Беремо 5 останніх новин для Слайдера
    latest_news = Post.objects.filter(is_published=True).order_by('-created_at')[:5]

    return render(request, 'home.html', {
        'upcoming_main': upcoming_main,
        'upcoming_second': upcoming_second,
        'past_main': past_main,
        'past_second': past_second,
        'latest_news': latest_news
    })


def news_list(request):
    """Список всіх новин"""
    all_news = Post.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'news_list.html', {'news': all_news})


def news_detail(request, pk):
    """Детальна сторінка новини"""
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'news_detail.html', {'post': post})


def team_list(request):
    """Список команди, розділений по групах"""
    # 1. Беремо всіх активних гравців
    members = Player.objects.filter(is_active=True)

    # 2. Розкладаємо їх по поличках
    context = {
        'groups': [
            {'title': 'Керівництво', 'people': members.filter(position='ADM')},
            {'title': 'Тренерський штаб', 'people': members.filter(position='COA')},
            {'title': 'Воротарі', 'people': members.filter(position='GK')},
            {'title': 'Захисники', 'people': members.filter(position='DF')},
            {'title': 'Півзахисники', 'people': members.filter(position='MF')},
            {'title': 'Нападники', 'people': members.filter(position='FW')},
            {'title': 'Медичний штаб', 'people': members.filter(position__in=['DOC', 'MAS'])},
            {'title': 'Персонал', 'people': members.filter(position__in=['MED', 'SPR'])},
        ]
    }
    return render(request, 'team_list.html', context)


def player_detail(request, pk):
    """Детальна сторінка гравця"""
    player = get_object_or_404(Player, pk=pk)
    return render(request, 'player_detail.html', {'player': player})


def fans_page(request):
    """Сторінка фанатів"""
    photos = FanPhoto.objects.all().order_by('-uploaded_at')
    return render(request, 'fans.html', {'photos': photos})


def register_view(request):
    """Реєстрація користувачів"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def about_club(request):
    return render(request, 'about.html')

def donate_page(request):
    return render(request, 'donate.html')

def partners_view(request):
    return render(request, 'partners.html')