from django import forms
from .models import Message,Image
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('contents',)

class SignUpForm(UserCreationForm):
    img = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ['username','email','password1','password2',] #'img'

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username',]
    def update(self, user):
        user.username = self.cleaned_data['username']
        user.save()

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email',]
    def update(self, user):
        user.email = self.cleaned_data['email']
        user.save()
