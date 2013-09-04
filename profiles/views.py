# Create your views here.
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.template.context import RequestContext
from profiles.forms import RegisterForm


def register(request, template="registration/register.html"):
    form = RegisterForm()

    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
    return render(request, template ,{'form':form})