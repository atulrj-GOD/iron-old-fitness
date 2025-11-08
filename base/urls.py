from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.login_view, name='login'),
    path('home/', views.login_view, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('payment/', views.payment_view, name='payment'),
    path('support/', views.support, name='support'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout_view, name='logout'),
    path('trainer/login/', views.trainer_login, name='trainer_login'),
    path('trainer/dashboard/<int:trainer_id>/', views.trainer_dashboard, name='trainer_dashboard'),
    path('trainer/register/', views.trainer_register, name='trainer_register'),
    path('locate/', views.locate, name='locate'),


]

