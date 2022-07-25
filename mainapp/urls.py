from django.urls import path

from .views import create_user_view, login_view, whoami

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', create_user_view, name='register'),
    # path('profile/', ProfileView.as_view(), name='profile'),
    path('whoami/', whoami, name='whoami')
]