from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('log-in/', views.login_user, name='login_user'),
    path('log-out/', views.logout_user, name='logout_user'),
]