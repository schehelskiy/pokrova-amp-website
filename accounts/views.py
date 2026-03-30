from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile # Переконайся, що імпортував модель Profile

@login_required
def profile_view(request):
    # Підстраховка: якщо це старий юзер, у якого ще немає профілю, створюємо його зараз
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # 1. Зберігаємо стандартні дані (ім'я, прізвище, email)
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()

        # 2. ЗБЕРІГАЄМО АВАТАРКУ
        # Перевіряємо, чи є в запиті файл з назвою 'avatar'
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
            profile.save()

        # Після збереження перезавантажуємо сторінку, щоб уникнути дублювання запиту
        return redirect('profile') # 'profile' - це name твоєї url-адреси профілю

    # Твоя логіка отримання замовлень (залиш її як було)
    orders = request.user.orders.all() # Приклад, як у тебе зараз отримуються замовлення

    context = {
        'orders': orders,
    }
    return render(request, 'profile.html', context)