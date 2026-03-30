from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Match, TournamentTable, MatchVote
from team.models import Player


def matches_page(request):
    """
    Сторінка календаря, результатів та турнірних таблиць.
    """
    upcoming_matches = Match.objects.filter(is_finished=False).order_by('date')
    finished_matches = Match.objects.filter(is_finished=True).order_by('-date')

    super_league = TournamentTable.objects.filter(league='SUPER').order_by('-points', '-wins', 'games_played')
    first_league = TournamentTable.objects.filter(league='FIRST').order_by('-points', '-wins', 'games_played')

    return render(request, 'matches.html', {
        'upcoming_matches': upcoming_matches,
        'finished_matches': finished_matches,
        'super_league': super_league,
        'first_league': first_league,
    })


def match_detail(request, pk):
    """
    Детальна сторінка матчу + Логіка голосування.
    """
    match = get_object_or_404(Match, pk=pk)

    # 1. ІСТОРІЯ ІГОР
    team1 = match.home_team
    team2 = match.away_team

    history = Match.objects.filter(
        (Q(home_team=team1) & Q(away_team=team2)) |
        (Q(home_team=team2) & Q(away_team=team1)),
        is_finished=True
    ).exclude(id=match.id).order_by('-date')

    wins = 0
    draws = 0
    losses = 0
    our_team_name = "Покрова АМП"

    for game in history:
        if game.home_score == game.away_score:
            draws += 1
        elif (game.home_team == our_team_name and game.home_score > game.away_score) or \
                (game.away_team == our_team_name and game.away_score > game.home_score):
            wins += 1
        else:
            losses += 1

    # 2. ГОЛОСУВАННЯ (ЛЕВ МАТЧУ)
    squad_players = match.squad.all()  # Гравці, яких адмін додав у склад
    user_voted = False

    if request.user.is_authenticated:
        user_voted = MatchVote.objects.filter(match=match, user=request.user).exists()

    # Підрахунок статистики голосів
    vote_stats = []
    total_votes = match.votes.count()

    if total_votes > 0:
        # Групуємо по гравцях і рахуємо кількість
        players_with_votes = match.votes.values('player').annotate(count=Count('player')).order_by('-count')

        for p_stat in players_with_votes:
            player_obj = Player.objects.get(pk=p_stat['player'])
            percent = (p_stat['count'] / total_votes) * 100
            vote_stats.append({
                'player': player_obj,
                'count': p_stat['count'],
                'percent': round(percent, 1)
            })

    return render(request, 'match_detail.html', {
        'match': match,
        'history': history,
        'wins': wins,
        'draws': draws,
        'losses': losses,
        # Змінні для голосування
        'squad_players': squad_players,
        'user_voted': user_voted,
        'vote_stats': vote_stats,
        'total_votes': total_votes,
    })


@login_required
def cast_vote(request, match_id, player_id):
    """
    Обробка голосу користувача.
    """
    match = get_object_or_404(Match, pk=match_id)
    player = get_object_or_404(Player, pk=player_id)

    # 1. Перевірка: чи матч завершено
    if not match.is_finished:
        messages.error(request, "Голосування доступне тільки для завершених матчів!")
        return redirect('match_detail', pk=match_id)

    # 2. Перевірка: чи вже голосував
    if MatchVote.objects.filter(match=match, user=request.user).exists():
        messages.warning(request, "Ви вже віддали свій голос у цьому матчі.")
        return redirect('match_detail', pk=match_id)

    # 3. Зберігаємо голос
    MatchVote.objects.create(match=match, user=request.user, player=player)
    messages.success(request, f"Ваш голос за {player.last_name} прийнято!")

    return redirect('match_detail', pk=match_id)