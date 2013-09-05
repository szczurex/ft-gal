from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.template.context import RequestContext
from profiles.forms import RegisterForm
from profiles.models import ActivationCode
from datetime import datetime


def register(request, template="registration/register.html"):
    form = RegisterForm()

    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            profile = form.save()
            code = ActivationCode().set_up(profile)
            code.save()
            # TODO: add mail to queue
            return redirect(register_success)
            
    return render(request, template ,{'form':form})


def register_success(request, template="registration/success.html"):
    return render(request, template)


def register_activate(request, key, template="registration/activate.html"):
    key = ActivationCode.objects.filter(key=key)
    if key:
        key = key[0]
        #check expiration
        if datetime.now() < key.expiration_date:
            # not expired, activate
            profile = key.profile
            profile.is_active = True
            profile.save()
            # do not delete key, change it's state
            #key.
            msg = "Account activated successfully!"
        else:
            # TODO: resend a new activation key.
            msg = "Activation key expired"
    else:
        msg = "Key does not exist in our database."
    # TODO: make template
    # TODO: parse and check key
    # TODO: activate account
    return render(request, template, {'msg':msg})


