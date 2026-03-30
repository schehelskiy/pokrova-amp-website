import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from shop.models import Order
from .models import Player
from django.db.models import Q, Case, When, Value, IntegerField

# Додаємо імпорт профілю
from accounts.models import Profile

def team_list(request):
    all_members = Player.objects.filter(is_active=True)

    pos_order = Case(
        When(position='DF', then=Value(1)),
        When(position='MF', then=Value(2)),
        When(position='FW', then=Value(3)),
        default=Value(4),
        output_field=IntegerField(),
    )

    team1_filter = Q(team='TEAM_1') | Q(team='') | Q(team__isnull=True)
    team2_filter = Q(team='TEAM_2')

    field_players = ['DF', 'MF', 'FW']
    staff_positions = ['DOC', 'MAS', 'MED', 'SPR']

    context = {
        # КОМАНДА 1
        't1_gk': all_members.filter(team1_filter, position='GK'),
        't1_players': all_members.filter(team1_filter, position__in=field_players).order_by(pos_order, 'number'),
        't1_staff': all_members.filter(team1_filter, position__in=staff_positions).order_by('position'),
        't1_coaches': all_members.filter(team1_filter, position='COA'),
        't1_management': all_members.filter(team1_filter, position='ADM'),

        # КОМАНДА 2
        't2_gk': all_members.filter(team2_filter, position='GK'),
        't2_players': all_members.filter(team2_filter, position__in=field_players).order_by(pos_order, 'number'),
        't2_staff': all_members.filter(team2_filter, position__in=staff_positions).order_by('position'),
        't2_coaches': all_members.filter(team2_filter, position='COA'),
        't2_management': all_members.filter(team2_filter, position='ADM'),

        # ЗАГАЛЬНОКЛУБНИЙ ШТАБ
        'club_management': all_members.filter(team='CLUB', position='ADM').order_by('position'),
        'club_staff': all_members.filter(team='CLUB', position__in=staff_positions).order_by('position'),
        'club_coaches': all_members.filter(team='CLUB', position='COA').order_by('position'),
    }

    return render(request, 'team_list.html', context)


def join_team(request):
    if request.method == 'POST':
        name = request.POST.get('name', 'Не вказано')
        phone = request.POST.get('phone', 'Не вказано')
        city = request.POST.get('city', '-')
        age = request.POST.get('age', '-')
        socials = request.POST.get('socials', '-')

        role = request.POST.get('role', 'Не обрано')
        veteran_status = request.POST.get('veteran_status', '-')
        injury_type = request.POST.get('injury_type', '-')
        game_level = request.POST.get('game_level', '-')
        position = request.POST.get('position', '-')

        about = request.POST.get('about', '').strip()
        if not about:
            about = "Немає додаткової інформації"

        msg = (
            f"🔥 <b>НОВА ЗАЯВКА В КОМАНДУ!</b>\n"
            f"------------------------------\n"
            f"👤 <b>Кандидат:</b> {name}\n"
            f"📞 <b>Телефон:</b> {phone}\n"
            f"🏙 <b>Місто:</b> {city}\n"
            f"🎂 <b>Вік:</b> {age}\n"
            f"🔗 <b>Соцмережі:</b> {socials}\n"
            f"------------------------------\n"
            f"📋 <b>ДЕТАЛІ ПРОФІЛЮ:</b>\n"
            f"🎖 <b>Роль:</b> {role}\n"
            f"🇺🇦 <b>Статус:</b> {veteran_status}\n"
            f"🏥 <b>Травма:</b> {injury_type}\n"
            f"⚽️ <b>Рівень:</b> {game_level}\n"
            f"🥅 <b>Позиція:</b> {position}\n"
            f"------------------------------\n"
            f"📝 <b>Додатково:</b>\n{about}"
        )

        token = settings.TELEGRAM_BOT_TOKEN
        chat_id = settings.TELEGRAM_CHAT_ID
        url = f"https://api.telegram.org/bot{token}/sendMessage"

        try:
            requests.post(url, data={'chat_id': chat_id, 'text': msg, 'parse_mode': 'HTML'})
            messages.success(request, "Ваша анкета прийнята!")
            return redirect('home')
        except Exception as e:
            messages.error(request, "Помилка відправки.")
    return render(request, 'join_team.html')


@login_required
def profile(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        if 'avatar' in request.FILES:
            user_profile.avatar = request.FILES['avatar']
            user_profile.save()

        messages.success(request, "Профіль успішно оновлено!")
        return redirect('profile')

    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'users/profile.html', {'orders': user_orders})