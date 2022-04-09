import json

from django.shortcuts import redirect, render

from django.contrib.auth import authenticate
from .forms import (
    SignUpForm,
    LoginForm,
    PostForm,
    NameChangeForm,
    EmailChangeForm,
    ImageChangeForm,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.contrib.auth.models import User
from django.db.models import Q, OuterRef, Subquery
from django.core.paginator import Paginator
from .models import Message, Image
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe


def index(request):
    return render(request, "myapp/index.html")


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            if request.FILES:
                img = form.cleaned_data.get("img")
                image = Image(image=img, user=user)
                image.save()
            else:
                img = "media/myapp/css/default.png"
                image = Image(image=img, user=user)
                image.save()
            return redirect("/")
    else:
        form = SignUpForm()
    return render(request, "myapp/signup.html", {"form": form})


class Login(LoginView):
    form_class = LoginForm
    template_name = "myapp/login.html"


class Logout(LoginRequiredMixin, LogoutView):
    template_name = "myapp/index.html"


@login_required(login_url="/login")
def talk_room(request, id):
    login_user = request.user
    login_user_name = str(login_user.username)
    companion = User.objects.get(id=id)
    msg = Message.objects.filter(
        Q(owner=login_user, receiver=companion)
        | Q(owner=companion, receiver=login_user)
    ).order_by("pub_date")
    if login_user.id < companion.id:
        room_name = str(login_user.id) + "_" + str(companion.id)
    else:
        room_name = str(companion.id) + "_" + str(login_user.id)
    params = {
        "me": login_user,
        "you": companion,
        "my_name_json": mark_safe(json.dumps(login_user_name)),
        "msg": msg,
        "room_name_json": mark_safe(json.dumps(room_name)),
        "form": PostForm(),
    }
    return render(request, "myapp/talk_room.html", params)


@login_required(login_url="/login")
def friends(request, num=1):
    login_user = request.user
    latest_msg = Message.objects.filter(
        Q(owner=OuterRef("pk"), receiver=login_user)
        | Q(owner=login_user, receiver=OuterRef("pk"))
    ).order_by("-pub_date")
    friends = (
        User.objects.exclude(id=login_user.id)
        .annotate(
            latest_msg_id=Subquery(latest_msg.values("pk")[:1]),
            latest_msg_content=Subquery(latest_msg.values("contents")[:1]),
            latest_msg_pub_date=Subquery(latest_msg.values("pub_date")[:1]),
        )
        .order_by("-latest_msg_id")
    )
    page = Paginator(friends, 30)
    params = {
        "friends": page.get_page(num),
        "me": login_user,
    }
    return render(request, "myapp/friends.html", params)


@login_required(login_url="/login")
def setting(request):
    return render(request, "myapp/setting.html")


class NameChange(LoginRequiredMixin, FormView):
    def get(self, request):
        params = {
            "title": "ユーザー名",
        }
        form = NameChangeForm()
        params["form"] = form
        return render(request, "myapp/valchange.html", params)

    def post(self, request):
        params = {
            "title": "ユーザーネーム",
        }
        form = NameChangeForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            User.objects.filter(username=request.user.username).update(
                username=username
            )
            return redirect("/redirect")
        else:
            params["form"] = form
            return render(request, "myapp/valchange.html", params)


class EmailChange(LoginRequiredMixin, FormView):
    def get(self, request):
        params = {
            "title": "メールアドレス",
        }
        form = EmailChangeForm()
        params["form"] = form
        return render(request, "myapp/valchange.html", params)

    def post(self, request):
        params = {
            "title": "メールアドレス",
        }
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            User.objects.filter(username=request.user.username).update(email=email)
            return redirect("/redirect")
        else:
            params["form"] = form
            return render(request, "myapp/valchange.html", params)


@login_required(login_url="/login")
def image_change(request):
    userImg = Image.objects.get(user=request.user)
    if request.method == "GET":
        form = ImageChangeForm(instance=request.user)
        params = {
            "user": request.user,
            "title": "プロフィール画像",
            "form": form,
            "userimg": userImg,
        }
        return render(request, "myapp/imgchange.html", params)

    elif request.method == "POST":
        params = {
            "title": "プロフィール画像",
        }
        form = ImageChangeForm(request.POST, request.FILES)
        if form.is_valid():
            userImg.image = form.cleaned_data.get("image")
            userImg.save()
            return redirect("/redirect")
        else:
            pass
        params = {
            "form": form,
            "userimg": userImg,
        }
        return render(request, "myapp/imgchange.html", params)


def redirection(request):
    return render(request, "myapp/redirect.html")


def chat(request):
    return render(request, "myapp/chat.html")
