from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


# Create your views here.

class StartPageView(View):
    def get(self, request):
        return render(request, 'social_news/start_page.html')

