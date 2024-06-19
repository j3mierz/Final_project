import pytest
import random
import string
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from social_news.models import Community, Profile, Post, Comment, Message


def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@pytest.fixture
def users():
    users = []
    for i in range(10):
        username = f'testuser{i}_{random_string(5)}'
        user = User.objects.create_user(username=username, password='12345')
        users.append(user)
    return users


@pytest.fixture
def profiles(users):
    profiles = []
    for user in users:
        profile_image = SimpleUploadedFile(name=f'test_image_{random_string(5)}.jpg', content=b'',
                                           content_type='image/jpeg')
        profile = Profile.objects.create(user=user, image=profile_image)
        profiles.append(profile)
    return profiles


@pytest.fixture
def communities(users):
    communities = []
    for i in range(10):
        name = f'Test Community {i} {random_string(5)}'
        description = f'A test community description with some extra text: {random_string(30)}.'
        user_creator = random.choice(users)
        community = Community.objects.create(name=name, description=description, user_creator=user_creator)
        community.users.set(random.sample(users, k=random.randint(1, len(users))))
        communities.append(community)
    return communities


@pytest.fixture
def posts(users, communities):
    posts = []
    for community in communities:
        for i in range(10):
            title = f'Test Post {i} {random_string(5)}'
            body = f'This is a test post with more detailed content: {random_string(50)}.'
            user_creator = random.choice(users)
            post = Post.objects.create(title=title, body=body, user_creator=user_creator, Community=community)
            posts.append(post)
    return posts


@pytest.fixture
def comments(users, posts):
    comments = []
    for post in posts:
        for i in range(10):
            body = f'This is a test comment with more detail: {random_string(50)}.'
            user_creator = random.choice(users)
            comment = Comment.objects.create(post=post, body=body, user_creator=user_creator)
            comments.append(comment)
    return comments


@pytest.fixture
def messages(users):
    messages = []
    for i in range(20):
        from_user = random.choice(users)
        to_user = random.choice([user for user in users if user != from_user])
        body = f'This is a test message with some unique content: {random_string(50)}.'
        message = Message.objects.create(from_user=from_user, body=body, to_user=to_user)
        messages.append(message)
    return messages


@pytest.fixture
def client_logged_in(users):
    from django.test import Client
    client = Client()
    client.login(username=users[0].username, password='12345')
    return client
