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
    path('setting', views.setting, name='setting'),
    path('logout',views.Logout.as_view(),name='logout_view'),
    path('pwchange',views.PasswordChangeView.as_view(),name='password_change'),
    path('pwchangedone',views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('namechange',views.NameChange.as_view(),name='namechange'),
    path('emailchange',views.EmailChange.as_view(),name='emailchange'),
    path('imagechange',views.image_change,name='imagechange'),
]
