from django.urls import path, include
from .views.auth_views import cust_login, cust_logout, home
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', cust_login, name='login'),
    path('logout/', cust_logout, name='logout'),
    path('index/', home, name='home'),
]