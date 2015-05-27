from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from gallery.models import Submission
from favourites.models import Favourite

from gallery.validators import MIMES_AUDIO, MIMES_IMAGE, MIMES_FLASH


def index(request, username, template="favourites/index.html"):
    profile = get_object_or_404(Profile, username__iexact=username)
    favourites = Favourite.objects.filter(profile=request.user,
                                          submission__deleted=False,
                                          submission__hidden=False)
    return render(request, template ,{'profile':profile,
                                      'favourites':favourites,
                                      'MIMES_AUDIO':MIMES_AUDIO,
                                      'MIMES_IMAGE':MIMES_IMAGE,
                                      'MIMES_FLASH':MIMES_FLASH})


@login_required
def add(request, username, submission_id):
    profile = get_object_or_404(Profile, username__iexact=username)
    submission = get_object_or_404(Submission,
                                   id=submission_id,
                                   profile=profile,
                                   deleted=False,
                                   hidden=False)
    
    fav, created = Favourite.objects.get_or_create(profile=request.user,
                                                   submission=submission)
    
    if not created:
        #we already had a fav. Remove it.
        fav.delete()
    
    return redirect('gallery:view',
                    username=profile.username,
                    submission_id=submission.id)