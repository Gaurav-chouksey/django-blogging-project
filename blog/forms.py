# blog/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post
from .models import Comment

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Provide a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image']  # include the image field


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
