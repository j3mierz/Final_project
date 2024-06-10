from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.views import View


# Create your views here.

class LoginView(View):
    def get(self, request):
        return render(request, "accounts/login_view.html")

    def post(self, request):
        username = request.POST('username')
        password = request.POST('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

class RegisterView(View):
    def get(self, request):
        return render(request, "accounts/register_view.html")
