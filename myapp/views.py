from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,authenticate
from . forms import SignUpForm, LoginForm, PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import(LoginView, LogoutView)
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Message

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = raw_password)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request,'myapp/signup.html',{'form':form})

class Login(LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'

    # if request.method == 'POST':
    #     frm = LoginForm()
    #     if frm.is_valid():
    #         return redirect('myapp/friends.html')
    # else:
    #     frm = LoginForm()
    # return render(request, "myapp/login.html",{'form':frm})

def talk_room(request,room_name): #urlsでそのように指定しているので第二引数がStringになる。
    data = Message.objects.all()
    form = PostForm()
    params={
        'form':PostForm(),
        "room_name": room_name,
        'data':data,
    }
    if request.method == 'POST':
        contents =request.POST['contents']
        msg=Message(owner=request.user, contents=contents)
    #         # msg.owner = request.user
    #         # msg.contents = contents 上と同じ。メッセージオブジェクトのインスタンス
        msg.save()
        print(request.POST)
        print(msg)
    #         # print(msg)
    #         #tableが来た
        params['form'] = PostForm(request.POST)
    else:
        form = PostForm()
    return render(request, "myapp/talk_room.html", params)

def friends(request,num=1):
    friends = User.objects.all().filter(~Q(username=request.user)).order_by('id').reverse() #Userそのまま使うのは非推奨らしい
    page = Paginator(friends,20)
    params ={
        'friends':page.get_page(num),
    }
    return render(request, "myapp/friends.html",params)

class Setting(LoginRequiredMixin, LogoutView):
    template_name="myapp/setting.html"

class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'myapp/login.html'
