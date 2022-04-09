from django.urls import path
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup_view, name="signup_view"),
    path("login", views.Login.as_view(), name="login_view"),
    path("friends/<int:num>", views.friends, name="friends"),
    path("friends", views.friends, name="friends"),
    path("talk_room/<int:id>", views.talk_room, name="talk_room"),
    path("setting", views.setting, name="setting"),
    path("logout", views.Logout.as_view(), name="logout_view"),
    path("pwchange", PasswordChangeView.as_view(), name="password_change"),
    path(
        "pwchangedone",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("namechange", views.NameChange.as_view(), name="namechange"),
    path("emailchange", views.EmailChange.as_view(), name="emailchange"),
    path("imagechange", views.image_change, name="imagechange"),
    path("redirect", views.redirection, name="redirect"),
    path("chat", views.chat, name="chat"),
]
