from django import forms

from social_news.models import Community, Post


class AddCommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'description']


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']