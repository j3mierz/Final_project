from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from social_news.models import Profile


# Create your views here.

class LoginView(View):
    def get(self, request):
        return render(request, "accounts/login_view.html")

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('start_page')
        return render(request, 'accounts/login_view.html', {"error": "Invalid username or password."})


class RegisterView(View):
    def get(self, request):
        return render(request, "accounts/register_view.html")

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        possword2 = request.POST.get('password2')
        if password == possword2 and password != "":
            user = User(username=username)
            user.set_password(password)
            user.save()
            login(request, user)
            Profile.objects.create(user=request.user, image="files/profiles/default.png")
            return redirect('login_view')
        return render(request, "accounts/register_view.html", {'error': "passwords do not match"})


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('login_view')
