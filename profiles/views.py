from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from profiles.forms import RegisterForm, WatchForm
from profiles.models import Profile, ActivationCode, ProfileWatch
from journals.models import Journal
from gallery.models import Submission
from datetime import datetime
from django.utils import timezone
from msg.views import queue_message
from gallery.validators import MIMES_AUDIO, MIMES_IMAGE, MIMES_FLASH

@login_required
def index(request):
    return redirect('profiles:userpage', request.user.username)


def userpage(request, username, template="profiles/index.html"):
    profile = get_object_or_404(Profile, username__iexact=username)
    
    last_journal = Journal.objects.filter(profile=profile, hidden=False, deleted=False)[:1]
    if last_journal:
        last_journal = last_journal[0]
    last_submissions = Submission.objects.filter(profile=profile, hidden=False, deleted=False)[:5]
        
    return render(request, template ,{'profile':profile,
                                      'last_journal':last_journal,
                                      'last_submissions':last_submissions,
                                      'MIMES_AUDIO':MIMES_AUDIO,
                                      'MIMES_IMAGE':MIMES_IMAGE,
                                      'MIMES_FLASH':MIMES_FLASH})


@login_required
def watch(request, username, template="profiles/watch.html"):
    target = get_object_or_404(Profile, username__iexact=username)
    profile = request.user
    
    if target == profile:
        # I understand that some people like to view themselves in the mirror, but...
        # Seriously, stop watching yourself.
        return redirect('profiles:userpage', profile.username)
    
    instance = None
    watch_inst = ProfileWatch.objects.filter(profile=profile,
                                             target=target)
    if watch_inst:
        instance = watch_inst[0]
    
    form = WatchForm(instance=instance)
    if request.POST:
        form = WatchForm(request.POST, instance=instance)
        watch = form.save(commit=False)
        watch.profile = profile
        watch.target = target
        watch.save()
        
        # TODO: leave a message "success"
        return redirect('profiles:userpage', target.username)
    
    return render(request, template ,{'profile':target,
                                      'form':form})

def register(request, template="registration/register.html"):
    form = RegisterForm()

    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            profile = form.save()
            code = ActivationCode().set_up(profile)
            code.save()
            queue_message(request, 'register_activate', code, profile.email)
            return redirect('profiles:register_success')
            
    return render(request, template ,{'form':form})


def register_success(request, template="registration/success.html"):
    return render(request, template)


def register_activate(request, key, template="registration/activate.html"):
    key = ActivationCode.objects.filter(key=key)
    if key:
        key = key[0]
        #check expiration
        if timezone.now() < key.expiration_date:
            # not expired
            #activated?
            if key.activated:
                msg = "Key already used."
            else:
                profile = key.profile
                profile.is_active = True
                profile.save()
                # do not delete key, change it's state
                key.activated = True
                key.save()
                msg = "Account activated successfully!"
        else:
            # TODO: resend a new activation key.
            msg = "Activation key has expired."
    else:
        msg = "Key does not exist in our database."

    return render(request, template, {'msg':msg})


