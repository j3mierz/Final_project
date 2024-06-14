from django import forms
from django.forms import ModelForm

from social_news.models import Community, Post, Profile


class AddCommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'description']


class AddPostForm(forms.Form):
    class Meta:
        model = Post
        fields = ['title', 'body']


class AddProfileForm(forms.Form):
    profile = forms.ImageField(required=True)