"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import LoginView, RegisterView
from social_news.views import StartPageView, CreateCommunityView, CommunityDetailView, AddPostView, PostDetailView, \
    UserProfileView, UpdatePostView, DeletePostView, JoinCommunityView
from django.conf.urls.static import static

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(), name='login_view'),
    path('register/', RegisterView.as_view(), name='register_view'),
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('', StartPageView.as_view(), name='start_page'),
    path('add_community/', CreateCommunityView.as_view(), name='add_community'),
    path('community_detail_view/<int:pk>/', CommunityDetailView.as_view(), name='community_detail_view'),
    path('community_detail_view/<int:pk>/add_post', AddPostView.as_view(), name='add_post_view'),
    path('post_detail/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('user_profile', UserProfileView.as_view(), name='user_profile'),
    path('update_post/<int:pk>/', UpdatePostView.as_view(), name='update_post'),
    path('delete_post/<int:pk>/', DeletePostView.as_view(), name='delete_post'),
    path('joincomm/<int:pk>/', JoinCommunityView.as_view(), name='join_comm'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
