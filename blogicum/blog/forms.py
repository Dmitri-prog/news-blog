from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django import forms

from .models import Post, Comment

User = get_user_model()


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'is_published', )
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        } 


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)