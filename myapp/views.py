from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,authenticate
from . forms import SignUpForm, LoginForm, PostForm , NameChangeForm, EmailChangeForm, ImageChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView ,PasswordChangeView,PasswordChangeDoneView
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Message,Image
from django.views.generic import FormView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

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
            if request.FILES:
                img = form.cleaned_data.get('img')
                image = Image(image=img, user=user)
                image.save()
            else:
                img = 'media/myapp/css/default.png'
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

@login_required(login_url ='/login')
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

@login_required(login_url ='/login')
def friends(request,num=1):
    friends = User.objects.all().filter(~Q(username=request.user))
    # data = []
    # for friend in friends:
    #     messages = Message.objects.all().filter(Q(owner = request.user,receiver = friend)|Q(owner__username = friend, receiver = request.user))
    #     try:
    #         data += messages.order_by('-pub_date')[0]
    #     except ObjectDoesNotExist:
    #         pass

    friendsOrder = friends.order_by('id').reverse() #Userそのまま使うのは非推奨らしい
    fpage = Paginator(friendsOrder,8)
    images = Image.objects.all().filter(~Q(user=request.user)).order_by('id').reverse()
    ipage = Paginator(images,8)
    params ={
        'data':fpage.get_page(num),
        'images':ipage.get_page(num),
    }
    return render(request, "myapp/friends.html",params)

@login_required(login_url ='/login')
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

@login_required(login_url ='/login')
def image_change(request):
    #どうしてもわからなかったのでsample参照
    try:
        userImg = Image.objects.get(user=request.user)
    except ObjectDoesNotExist:
        userImg = Image.objects.none()
    if request.method == 'GET':
        params = {"title":"プロフィール画像",}
        form = ImageChangeForm(instance=request.user) #userの情報が入ったformを参照
        params["form"] = form
        params["userimg"] = userImg
        return render(request, 'myapp/imgchange.html', params)

    elif request.method == "POST":
        params = {"title":"プロフィール画像",}
        form = ImageChangeForm(request.POST,request.FILES)
        print(request.POST)
        print(request.FILES) #なんで空になるの？
        if form.is_valid():
            userImg.image = form.cleaned_data.get("image")
            # img_obj = Image.objects.get(image=newImage,user = request.user)
            # img_obj.image = newImage
            userImg.save()
            return redirect('/setting')
        else:
            pass
        params ={
            "form":form,
            "userimg":userImg,
        }
        return render(request, 'myapp/imgchange.html', params)