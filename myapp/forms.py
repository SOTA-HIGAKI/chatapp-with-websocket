from django import forms
from .models import Message,Friend,Document
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PostForm(forms.Form):
    content = forms.CharField(max_length = 500)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100,label='Eメールアドレス')
    img =forms.ImageField()
    class Meta:
        model = User
        fields = ('username','email','password1','password2','img',)
class DocumentForm(forms.ModelForm):
    class Meta:
        model =Document
        fields = ('photo',)
# class LoginForm(forms.Form):
