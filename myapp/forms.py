from django import forms
from .models import Message,Document
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class PostForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('contents',)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100,label='Eメールアドレス')
    # img = forms.ImageField(upload_to = requires = False)
    class Meta:
        model = User
        fields = ('username','email','password1','password2',) #'img'
class DocumentForm(forms.ModelForm):
    class Meta:
        model =Document
        fields = ('photo',)

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
