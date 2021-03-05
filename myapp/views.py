from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,authenticate
from . forms import SignUpForm, LoginForm, PostForm , NameChangeForm, EmailChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView ,PasswordChangeView,PasswordChangeDoneView
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Message,Image
from django.views.generic import FormView

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST,request.FILES)
        print(request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = raw_password)
            img = form.cleaned_data.get('img')
            image = Image(image=img, user=user)
            image.save()
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request,'myapp/signup.html',{'form':form})

class Login(LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'

class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'myapp/index.html'

def talk_room(request,room_name): #urlsでそのように指定しているので第二引数がStringになる。
    form = PostForm()
    #Userから取得　Str→obj
    rNameUser = get_object_or_404(User,username = room_name)
    if request.method == 'POST':
        contents =request.POST['contents']
        msg=Message(owner=request.user, contents=contents,receiver = rNameUser)
    #         # msg.owner = request.user
    #         # msg.contents = contents 上と同じ。メッセージオブジェクトのインスタンス
        msg.save()
    #         #print form はtableが来た
        form = PostForm()
    else:
        form = PostForm()
    data = Message.objects.all().filter(Q(owner = request.user,receiver = rNameUser)|Q(owner__username = rNameUser, receiver = request.user))\
    .order_by('pub_date')
    #request.user、owner,receiverはuserobj,room_nameはStringなのでおかしくなってしまう

    params={
        "form":form,
        "room_name": room_name,
        'data':data, #dataを絞り込む必要性(解決)
    }
    return render(request, "myapp/talk_room.html", params)

def friends(request,num=1):
    friends = User.objects.all().filter(~Q(username=request.user)).order_by('id').reverse() #Userそのまま使うのは非推奨らしい
    page = Paginator(friends,20)
    params ={
        'friends':page.get_page(num),
    }
    return render(request, "myapp/friends.html",params)

def setting(request):
    return render(request, "myapp/setting.html")

# class PWChange(LoginRequiredMixin,PasswordChangeView):
#     template_name = ''

# class PWChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
#     template_name = ''

class NameChange(LoginRequiredMixin,FormView):
    def get(self, request, *args, **kwargs):
        params = {"title":"ユーザー名",}
        form = NameChangeForm()
        params["form"] = form
        return render(request, 'myapp/valchange.html', params)

    def post(self, request, *args, **kwargs):
        params = {"title":"ユーザーネーム",}
        form = NameChangeForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            user_obj = User.objects.get(username=request.user.username)
            user_obj.username = username
            user_obj.save()
            return redirect('/setting')
        else:
            params["form"] = form
            return render(request, 'myapp/valchange.html', params)

class EmailChange(LoginRequiredMixin,FormView):
    def get(self, request, *args, **kwargs):
        params = {"title":"メールアドレス",}
        form = EmailChangeForm()
        params["form"] = form
        return render(request, 'myapp/valchange.html', params)

    def post(self, request, *args, **kwargs):
        params = {"title":"メールアドレス",}
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user_obj = User.objects.get(email=request.user.email)
            user_obj.email = email
            user_obj.save()
            return redirect('/setting')
        else:
            params["form"] = form
            return render(request, 'myapp/valchange.html', params)