import json

from django.shortcuts import redirect, render

from django.contrib.auth import login, authenticate
from . forms import SignUpForm, LoginForm, PostForm , NameChangeForm, EmailChangeForm, ImageChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.models import User
from django.db.models import Q, OuterRef, Subquery
from django.core.paginator import Paginator
from .models import Message,Image
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST,request.FILES)
        # print(request.FILES)
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
def talk_room(request,id): #urlsでそのように指定しているので第二引数がStringになる。
    # form = PostForm()
    user_me = request.user
    my_name = str(user_me.username)
    user_you = User.objects.get(id=id)
    msg = Message.objects.filter( Q(owner=user_me,receiver=user_you) | Q(owner=user_you,receiver=user_me) ).order_by("pub_date")
    if user_me.id < user_you.id:
        room_name = str(user_me.id) + '_' + str(user_you.id)
    else:
        room_name = str(user_you.id) + '_' + str(user_me.id)
    #Userから取得　Str→obj
    # rNameUser = get_object_or_404(User,username = room_name)
    # if request.method == 'POST':
    #     contents =request.POST['contents']
    #     msg=Message(owner=request.user, contents=contents,receiver = rNameUser)
    # #         # msg.owner = request.user
    # #         # msg.contents = contents 上と同じ。メッセージオブジェクトのインスタンス
    #     msg.save()
    # #         #print form はtableが来た
    #     form = PostForm()
    # else:
    #     form = PostForm()
    # data = Message.objects.all().filter(Q(owner = request.user,receiver = rNameUser)|Q(owner__username = rNameUser, receiver = request.user))\
    # .order_by('pub_date')
    #request.user、owner,receiverはuserobj,room_nameはStringなのでおかしくなってしまう

    params = {
        'me': user_me,
        'you': user_you,
        'my_name_json': mark_safe(json.dumps(my_name)),
        'msg': msg,
        'room_name_json': mark_safe(json.dumps(room_name)),
        'form': PostForm(),
    }
    return render(request, "myapp/talk_room.html", params)

@login_required(login_url ='/login')
def friends(request,num=1):

    #friendsとtalkroomの順番がそもそも結びついていないので困難。。。
    # data = []
    # for friend in friends:
    #     messages = Message.objects.all().filter(Q(owner = request.user,receiver = friend)|Q(owner__username = friend, receiver = request.user))
    #     try:
    #         data += messages.order_by('-pub_date')[0]
    #     except ObjectDoesNotExist:
    #         pass

    # friendsOrder = friends.order_by('id').reverse() #Userそのまま使うのは非推奨らしい
    # fpage = Paginator(friendsOrder,8)
    # images = Image.objects.filter(~Q(user=request.user))
    # ipage = Paginator(images,8)


    # friends = User.objects.filter(~Q(username=request.user))
    # latest_message = Message.objects.filter(Q(owner = request.user,receiver = OuterRef('pk'))|Q(owner = OuterRef('pk'), receiver = request.user))\
    # .order_by('-pub_date') #User id をOuterreferしている
    # friendsAnnotate = User.objects.exclude(id=request.user.id).annotate( #filterは一つずつとってきているイメージで、そのたびにアノテートが発動し○○さんのIDが上のOuterRefに入っているイメージ。
    #     latest_message_id = Subquery(
    #         latest_message.values('pk')[:1]
    #     ),
    #     latest_message_content = Subquery(
    #         latest_message.values('contents')[:1] #friendsがparameterでテンプレートに渡されているので、その中に入っているこれも渡される。なんて便利！
    #     ),
    #     latest_message_pub_date = Subquery(
    #         latest_message.values('pub_date')[:1]
    #     ),
    # ).order_by("-latest_message_pub_date")
    # friendsPage = Paginator(friendsAnnotate,8)
    # params ={
    #     "user":request.user,
    #     "friends":friendsPage.get_page(num),
    #     # 'data':fpage.get_page(num),
    #     # 'images':ipage.get_page(num),
    # }

    # my_name = str(user_me.username)
    # user_you = User.objects.get(id=user_me.id)
    # if user_me.id < user_you.id:
    #     room_name = str(user_me.id) + '_' + str(user_you.id)
    # else:
    #     room_name = str(user_you.id) + '_' + str(user_me.id)
    user_me = request.user
    latest_msg = Message.objects.filter( Q(owner=OuterRef("pk"),receiver=user_me) | Q(owner=user_me,receiver=OuterRef("pk")) ).order_by('-pub_date')
    user_qs = (User.objects
        .exclude(id=user_me.id)
        .annotate(
            latest_msg_id=Subquery(
                latest_msg.values("pk")[:1]
            ),
            latest_msg_content=Subquery(
                latest_msg.values("contents")[:1]
            ),
            latest_msg_pub_date=Subquery(
                latest_msg.values("pub_date")[:1]
            ),
        )
        .order_by("-latest_msg_id")
    )
    page = Paginator(user_qs,30)
    params = {
        'friends': page.get_page(num),
        'me': user_me,
    }
    return render(request, "myapp/friends.html",params)

@login_required(login_url ='/login')
def setting(request):
    return render(request, "myapp/setting.html")

# class PWChange(LoginRequiredMixin,PasswordChangeView):
#     template_name = ''

# class PWChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
#     template_name = ''LoginRequiredMixin,

class NameChange(LoginRequiredMixin,FormView):
    def get(self, request):
        params = {"title":"ユーザー名",}
        form = NameChangeForm()
        params["form"] = form
        return render(request, 'myapp/valchange.html', params)

    def post(self, request):
        params = {"title":"ユーザーネーム",}
        form = NameChangeForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            user_obj = User.objects.get(username=request.user.username)
            user_obj.username = username
            user_obj.save()
            return redirect('/redirect')
        else:
            params["form"] = form
            return render(request, 'myapp/valchange.html', params)

class EmailChange(LoginRequiredMixin,FormView):
    def get(self, request):
        params = {"title":"メールアドレス",}
        form = EmailChangeForm()
        params["form"] = form
        return render(request, 'myapp/valchange.html', params)

    def post(self, request):
        params = {"title":"メールアドレス",}
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user_obj = User.objects.get(username=request.user.username)
            user_obj.email = email
            user_obj.save()
            return redirect('/redirect')
        else:
            params["form"] = form
            return render(request, 'myapp/valchange.html', params)

@login_required(login_url ='/login')
def image_change(request):
    #どうしてもわからなかったのでsample参照
    # try:
    #     userImg = Image.objects.get(user=request.user)
    # except ObjectDoesNotExist:
    #     userImg = Image.objects.none()
    userImg = Image.objects.get(user=request.user)
    if request.method == 'GET':
        form = ImageChangeForm(instance=request.user) #userの情報が入ったformを参照
        params ={
            "user":request.user,
            "title":"プロフィール画像",
            "form":form,
            "userimg":userImg,
        }
        return render(request, 'myapp/imgchange.html', params)

    elif request.method == "POST":
        params = {"title":"プロフィール画像",}
        form = ImageChangeForm(request.POST,request.FILES)
        # print(request.POST)
        # print(request.FILES) #↓のとき、なんで空になるの？あとでgitで確認。
        if form.is_valid():
            userImg.image = form.cleaned_data.get("image")
            # img_obj = Image.objects.get(image=newImage,user = request.user)
            # img_obj.image = newImage
            userImg.save()
            return redirect('/redirect')
        else:
            pass
        params ={
            "form":form,
            "userimg":userImg, #意味ある？
        }
        return render(request, 'myapp/imgchange.html', params)


def redirection(request):
    return render(request,'myapp/redirect.html')

def chat(request):
    return render(request,'myapp/chat.html')