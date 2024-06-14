from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from social_news.forms import AddCommunityForm, AddPostForm, AddProfileForm
from social_news.models import Community, Post, Comment, Profile


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


class CommunityDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        community = Community.objects.get(id=pk)
        posts = Post.objects.filter(Community=community)
        profile = Profile.objects.get(user=request.user)
        return render(request, "social_news/community_detail_view.html", {'community': community,
                                                                          'posts': posts,
                                                                          'profile': profile})


class AddPostView(LoginRequiredMixin, CreateView):
    def get(self, request, pk):
        form = AddPostForm(request.POST)
        return render(request, "social_news/form.html", {'form': form})

    def post(self, request, pk):
        form = AddPostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['body']
            user_creator = request.user
            community = Community.objects.get(id=pk)
            Post.objects.create(title=title, body=description, user_creator=user_creator, Community=community)
            return redirect('community_detail_view', pk=community.id)
        return render(request, "social_news/form.html", {'form': form})


class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        comments = Comment.objects.filter(post=post)
        return render(request, "social_news/post_detail_view.html", {'post': post,
                                                                     'comments': comments})

    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        comment = request.POST.get('comment')
        user_creator = request.user
        Comment.objects.create(post=post, body=comment, user_creator=user_creator)
        comments = Comment.objects.filter(post=post)
        return render(request, "social_news/post_detail_view.html", {'post': post,
                                                                     'comments': comments})


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        form = AddProfileForm()
        return render(request, "social_news/user_profile.html", {'profile': profile,
                                                                 'form': form})

    def post(self, request):
        form = AddProfileForm(request.POST, request.FILES)
        if form.is_valid():
            Profile.objects.get(user=request.user).delete()
            profile = request.FILES['profile']
            Profile.objects.create(user=request.user, image=profile).save()
            return redirect('start_page')
        return render(request, "social_news/user_profile.html", {'form': form})


class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'body']
    template_name = "social_news/form.html"

    def get_success_url(self):
        return reverse_lazy('post_detail', args=(self.get_object().pk,))
