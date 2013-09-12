from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from journals.models import Journal
from journals.forms import JournalForm
from django.http import HttpResponseForbidden


@login_required
def index(request, username=None, template="journals/index.html"):
    profile = get_object_or_404(Profile, username__iexact=username)
    journals = Journal.objects.filter(profile = profile, deleted=False)
    return render(request, template ,{'profile':profile,
                                      'journals':journals})


@login_required
def mine(request, template="journals/mine.html"):
    profile = request.user
    journals = Journal.objects.filter(profile = profile, deleted=False)
    return render(request, template ,{'profile':profile,
                                      'journals':journals})


@login_required
def edit(request, id=None, template="journals/edit.html"):
    profile = request.user
    instance = None
    if id:
        instance = get_object_or_404(Journal, id=id)
    
    if instance:
        if instance.profile != profile:
            # GTFO, not yours.
            return HttpResponseForbidden()
        
    form = JournalForm(instance=instance)
    
    if request.POST:
        form = JournalForm(request.POST, instance=instance)
        if form.is_valid():
            journal = form.save(commit=False)
            journal.profile = profile
            journal.save()
            # TODO: success message
            return redirect('journals:mine')
    
    return render(request, template ,{'profile':profile,
                                      'form':form,
                                      'instance':instance})
    
    
@login_required
def delete(request, id, template="journals/delete.html"):
    profile = request.user
    journal = get_object_or_404(Journal, id=id)
    
    if journal.profile != profile:
        # GTFO, not yours.
        return HttpResponseForbidden()
    
    journal.deleted = True
    journal.save()
    # TODO: success message
    return redirect('journals:mine')