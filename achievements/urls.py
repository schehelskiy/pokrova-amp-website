from django.urls import path
from . import views

urlpatterns = [
    # Це головна сторінка додатка (яка буде доступна за адресою /achievements/)
    path('', views.achievements_list, name='achievements_list'),
]