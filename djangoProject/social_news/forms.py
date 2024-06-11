from django import forms

from social_news.models import Community


class AddCommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'description']