from django.urls import path,include
from.views import *

app_name = 'users'
urlpatterns = [
    path('register/',user_register,name='user_register'),
    path('login/',user_login,name='user_login'),
    path('logout/',user_logout,name='user_logout'),
    path('profile/', profile, name='profile'),
    path('update/profile/',update_profile,name='update_profile'),
    path('delete/user/',delete_user,name='delete_user'),
    path('forgot_password/',forgot_password,name='forgot_password'),
    path('change_password/<token>/',change_password,name='change_password'),
]