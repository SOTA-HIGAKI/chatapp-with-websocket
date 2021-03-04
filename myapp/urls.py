from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.Login.as_view(), name='login_view'),
    path('friends/<int:num>', views.friends, name='friends'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<str:room_name>', views.talk_room, name='talk_room'),
    path('setting', views.Setting, name='setting'),
]
