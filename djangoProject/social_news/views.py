from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from social_news.forms import AddCommunityForm
from social_news.models import Community


# Create your views here.

class StartPageView(LoginRequiredMixin, View):
    def get(self, request):
        communities = Community.objects.all()
        return render(request, 'social_news/start_page.html', {'communities': communities})


class CreateCommunityView(CreateView):
    def get(self, request):
        form = AddCommunityForm
        return render(request, "social_news/form.html", {'form': form})
    def post(self, request):
        form = AddCommunityForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            user_creator = request.user
            Community.objects.create(name=name, description=description, user_creator=user_creator)
            return redirect('start_page')
        return render(request, "social_news/form.html", {'form': form})