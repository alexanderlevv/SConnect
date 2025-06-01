from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Track

class RegisterForm(UserCreationForm):
    avatar = forms.ImageField(required=False)
    nickname = forms.CharField(max_length=32)

    class Meta:
        model = User
        fields = ('username', 'nickname', 'avatar', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    pass

class TrackUploadForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'audio_file', 'cover_image', 'description']
