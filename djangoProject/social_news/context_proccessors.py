from social_news.models import Profile


def Profile_CTX(request):
    return {
        "Profile_CTX": Profile.objects.all()
    }
