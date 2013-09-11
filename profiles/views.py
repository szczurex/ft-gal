from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.template.context import RequestContext
from profiles.forms import RegisterForm
from profiles.models import Profile, ActivationCode
from datetime import datetime
from django.utils import timezone
from messages.views import queue_message
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return redirect('profiles:userpage', request.user.username)


@login_required
def userpage(request, username, template="profiles/index.html"):
    profile = get_object_or_404(Profile, username__iexact=username)
    return render(request, template ,{'profile':profile})


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


