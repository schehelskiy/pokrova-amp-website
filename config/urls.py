from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Імпорти з додатка TEAM
from team.views import team_list, join_team, profile

# Імпорти з додатка PAGES (ОСЬ ТУТ Я ДОДАВ partners_view)
from pages.views import (
    home,
    about_club,
    donate_page,
    player_detail,
    fans_page,
    register_view,
    partners_view
)

# Імпорти з додатка MATCHES
from matches.views import matches_page, match_detail, cast_vote

# Імпорти з додатка NEWS
from news.views import news_list, news_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('allauth.urls')),

    # Партнери (тепер без помилок)
    path('partners/', partners_view, name='partners'),

    # Новини
    path('news/', news_list, name='news_list'),
    path('news/<int:pk>/', news_detail, name='news_detail'),

    # Команда
    path('team/', team_list, name='team_list'),
    path('team/<int:pk>/', player_detail, name='player_detail'),

    # Матчі
    path('matches/', matches_page, name='matches_page'),
    path('matches/<int:pk>/', match_detail, name='match_detail'),
    path('matches/<int:match_id>/vote/<int:player_id>/', cast_vote, name='cast_vote'),

    # Магазин та інше
    path('shop/', include('shop.urls')),
    path('fans/', fans_page, name='fans_page'),
    path('register/', register_view, name='register'),
    path('join/', join_team, name='join_team'),
    path('profile/', profile, name='profile'),
    path('about/', about_club, name='about_club'),
    path('donate/', donate_page, name='donate_page'),

    path('gallery/', include('gallery.urls')),
    path('achievements/', include('achievements.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)