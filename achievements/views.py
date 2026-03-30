from django.shortcuts import render
from .models import Achievement

# Назва має бути в точності achievements_list
def achievements_list(request):
    achievements = Achievement.objects.all()
    return render(request, 'achievements/achievements_list.html', {'achievements': achievements})