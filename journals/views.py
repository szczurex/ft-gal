from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from profiles.models import Profile


@login_required
def index(request, username=None, template="journals/index.html"):
    profile = get_object_or_404(Profile, username__iexact=username)
    return render(request, template ,{'profile':profile})
