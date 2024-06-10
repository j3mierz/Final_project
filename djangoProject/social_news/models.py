from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')


class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    user_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)


class Post(models.Model):
    title = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    body = models.TextField()
    user_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_me')
    body = models.TextField()
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_me')
    created_at = models.DateTimeField(auto_now_add=True)

