from django import forms
from .models import Post

class Newsform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'categories']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'categories']