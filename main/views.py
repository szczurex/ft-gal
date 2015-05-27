# Create your views here.
from django.shortcuts import render


def index(request, template="main/index.html"):
    return render(request, template, {})