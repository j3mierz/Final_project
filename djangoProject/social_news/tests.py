import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from social_news.models import Community, Post, Profile, Comment, Message


# TESTSING OF MODELS INSTANCES CREATION
####################################################################################
@pytest.mark.django_db
def test_profile_creation(profiles, users):
    assert len(profiles) == len(users)
    for profile, user in zip(profiles, users):
        assert profile.user == user


@pytest.mark.django_db
def test_community_creation(communities, users):
    assert len(communities) == 10
    for community in communities:
        assert community.user_creator in users


@pytest.mark.django_db
def test_post_creation(posts, communities, users):
    assert len(posts) == len(communities) * len(users)
    for post in posts:
        assert post.Community in communities
        assert post.user_creator in users


@pytest.mark.django_db
def test_comment_creation(comments, posts, users):
    assert len(comments) == len(posts) * len(users)
    for comment in comments:
        assert comment.post in posts
        assert comment.user_creator in users


@pytest.mark.django_db
def test_message_creation(messages, users):
    assert len(messages) == 20
    for message in messages:
        assert message.from_user in users
        assert message.to_user in users
        assert message.from_user != message.to_user


#######################################################################################################
@pytest.mark.django_db
def test_start_page_view_get(client_logged_in, communities, users):
    response = client_logged_in.get(reverse('start_page'))
    assert response.status_code == 200
    assert 'communities' in response.context
    assert 'users' in response.context


@pytest.mark.django_db
def test_start_page_view_post(client_logged_in, users, communities):
    communities = communities[0]
    search_term = 'Test Community 1'
    data = {'search': search_term}
    response = client_logged_in.post(reverse('start_page'), data)
    assert response.status_code == 200
    assert 'communities' in response.context
    assert 'users' in response.context
    found_communities = response.context['communities']
    assert len(found_communities) == 1
    for community in found_communities:
        assert search_term in community.name


@pytest.mark.django_db
def test_start_page_view_post_not_found(client_logged_in, users, communities):
    communities = communities[0]
    search_term = 'no community'
    data = {'search': search_term}
    response = client_logged_in.post(reverse('start_page'), data)
    assert response.status_code == 200
    assert 'message' in response.context
    assert 'users' in response.context
    assert "communities" not in response.context


@pytest.mark.django_db
def test_create_community_view_post(client_logged_in, users):
    data = {'name': 'New Community', 'description': 'A new community'}
    response = client_logged_in.post(reverse('add_community'), data)
    assert response.status_code == 302
    assert Community.objects.filter(name='New Community').exists()


@pytest.mark.django_db
def test_create_community_view_post_wrong_data(client_logged_in, users):
    data = {'name': 'New Community', '': ''}  # WRONG DATA
    response = client_logged_in.post(reverse('add_community'), data)
    assert response.status_code == 200
    assert 'form' in response.context


@pytest.mark.django_db
def test_create_community_view_get(client_logged_in, users):
    response = client_logged_in.get(reverse('add_community'))
    assert response.status_code == 200
    assert 'form' in response.context


@pytest.mark.django_db
def test_community_detail_view_get(communities, users, profiles, posts):
    for community, user in zip(communities, users):
        client = Client()
        client.login(username=user.username, password='12345')
        response = client.get(reverse('community_detail_view', args=[community.id]))
        assert response.status_code == 200
        assert 'community' in response.context
        assert 'posts' in response.context
        assert 'profile' in response.context
        assert 'joined' in response.context
        if response.context['joined'] == 'true':
            assert community.users.filter(id=user.id).exists()
        else:
            assert not community.users.filter(id=user.id).exists()


@pytest.mark.django_db
def test_add_post_view_get(client_logged_in, communities):
    for community in communities:
        response = client_logged_in.get(reverse('add_post_view', args=[community.id]))
        assert response.status_code == 200
        assert 'form' in response.context


@pytest.mark.django_db
def test_add_post_view_post(client_logged_in, communities, users):
    community = communities[0]
    data = {'title': 'New Post', 'body': 'This is a new post'}
    response = client_logged_in.post(reverse('add_post_view', args=[community.id]), data)
    assert response.status_code == 302
    assert Post.objects.filter(title='New Post').exists()


@pytest.mark.django_db
def test_add_post_view_post_wrong_data(client_logged_in, communities, users):
    community = communities[0]
    data = {'title': 'New Post', '': 'This is a new post'}  # WRONG DATA
    response = client_logged_in.post(reverse('add_post_view', args=[community.id]), data)
    assert response.status_code == 200
    assert 'form' in response.context


@pytest.mark.django_db
def test_post_detail_view_get(client_logged_in, posts):
    for post in posts:
        response = client_logged_in.get(reverse('post_detail', args=[post.id]))
        assert response.status_code == 200
        assert 'post' in response.context
        assert 'comments' in response.context


@pytest.mark.django_db
def test_post_detail_view_post(client_logged_in, posts):
    for post in posts:
        data = {'comment': 'comment_body'}
        response = client_logged_in.post(reverse('post_detail', args=[post.id]), data)
        assert response.status_code == 200
        assert 'post' in response.context
        assert 'comments' in response.context


@pytest.mark.django_db
def test_user_profile_view_get(users, profiles):
    for user in users:
        client = Client()
        client.login(username=user.username, password='12345')
        response = client.get(reverse('user_profile'))
        assert response.status_code == 200
        assert 'profile' in response.context
        assert 'form' in response.context
        assert 'joined' in response.context
        assert 'communities' in response.context

        profile = response.context['profile']
        joined = response.context['joined']

        assert profile.user == user
        assert set(joined) == set(Community.objects.filter(users=user))


@pytest.mark.django_db
def test_user_profile_view_post(users, profiles):
    for user in users:
        client = Client()
        client.login(username=user.username, password=user.password)
        image = "test_image.jpg"
        data = {
            'profile': image,
        }
        response = client.post(reverse('user_profile'), data, format='multipart')
        assert response.status_code == 302
        assert Profile.objects.filter(user=user).exists()
        profile = Profile.objects.get(user=user)


@pytest.mark.django_db
def test_update_post_view_get(client_logged_in, posts):
    for post in posts:
        response = client_logged_in.get(reverse('update_post', args=[post.id]))
        assert response.status_code == 200
        assert 'form' in response.context
        form = response.context['form']
        assert form.instance == post


@pytest.mark.django_db
def test_update_post_view_post(client_logged_in, posts):
    for post in posts:
        data = {
            'title': 'Updated Post Title',
            'body': 'Updated Post Body',
        }
        response = client_logged_in.post(reverse('update_post', args=[post.id]), data)
        assert response.status_code == 302
        assert response.url == reverse('post_detail', args=[post.id])
        post.refresh_from_db()
        assert post.title == 'Updated Post Title'
        assert post.body == 'Updated Post Body'


@pytest.mark.django_db
def test_delete_post_view_get(client_logged_in, posts):
    for post in posts:
        response = client_logged_in.get(reverse('delete_post', args=[post.id]))
        assert response.status_code == 200
        assert 'post' in response.context
        assert response.context['post'] == post


@pytest.mark.django_db
def test_delete_post_view_post(client_logged_in, posts):
    for post in posts:
        response = client_logged_in.post(reverse('delete_post', args=[post.id]))
        assert response.status_code == 302
        assert response.url == reverse('start_page')
        with pytest.raises(Post.DoesNotExist):
            Post.objects.get(id=post.id)


@pytest.mark.django_db
def test_join_community_view_get(client_logged_in, communities, users):
    community = communities[0]
    response = client_logged_in.get(reverse('join_comm', args=[community.id]))
    assert response.status_code == 302
    assert community.users.filter(id=users[0].id).exists()


@pytest.mark.django_db
def test_messages_view_get(client_logged_in, users, messages, profiles):
    for another_user in users:
        if another_user == client_logged_in:
            continue
        response = client_logged_in.get(reverse('messages', args=[another_user.id]))
        assert response.status_code == 200
        assert 'users' in response.context
        assert 'to_user' in response.context
        assert 'to_user_profile' in response.context
        assert 'messages' in response.context


@pytest.mark.django_db
def test_messages_view_post(client_logged_in, users, profiles):
    logged_in_user = users[0]
    for to_user in users:
        if to_user == client_logged_in:
            continue
    data = {
        'message': 'Test message content',
    }
    response = client_logged_in.post(reverse('messages', args=[to_user.id]), data)
    assert response.status_code == 200
    assert 'users' in response.context
    assert 'to_user' in response.context
    assert 'to_user_profile' in response.context
    assert 'messages' in response.context
    assert response.context['to_user'] == to_user
    assert response.context['to_user_profile'].user == to_user
    assert Message.objects.filter(from_user=logged_in_user, to_user=to_user, body='Test message content').exists()


@pytest.mark.django_db
def test_login_view_post(client, users):
    user = users[1]
    login_data = {
        'username': user.username,
        'password': user.password,
    }
    response = client.post(reverse('login_view'), login_data)
    assert response.status_code == 200
