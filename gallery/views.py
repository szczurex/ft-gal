from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from gallery.forms import SubmissionForm, CommentForm
from gallery.models import Submission, Submission_Comment
from gallery.validators import MIMES_AUDIO, MIMES_IMAGE, MIMES_FLASH


def index(request, username, template="gallery/index.html"):
    profile = get_object_or_404(Profile, username__iexact=username)
    submissions = Submission.objects.filter(profile=profile,
                                           deleted=False,
                                           hidden=False)
    
    return render(request, template ,{'profile':profile,
                                      'submissions':submissions,
                                      'MIMES_AUDIO':MIMES_AUDIO,
                                      'MIMES_IMAGE':MIMES_IMAGE,
                                      'MIMES_FLASH':MIMES_FLASH})


def view(request, username, submission_id, template="gallery/view.html"):
    profile = get_object_or_404(Profile, username__iexact=username)
    submission = get_object_or_404(Submission, 
                                   id=submission_id,
                                   profile=profile,
                                   deleted=False,
                                   hidden=False)
    
    comments = Submission_Comment.objects.filter(submission=submission,
                                                 deleted=False)
    form = None
    if request.user.is_authenticated():
        form = CommentForm()
    
    if request.POST:
        if form:
            #TODO: check if user can post (privacy/blacklist/etc)
            #TODO: replying to a comment
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.profile = request.user
                comment.submission = submission
                #TODO
                #comment.comment = parent_comment
                comment.save()
                #IDEA: redirect with a link to the comment?
                return redirect('gallery:view',
                                username=profile.username,
                                submission_id=submission.id)
    
    return render(request, template ,{'profile':profile,
                                      'submission':submission,
                                      'form':form,
                                      'comments':comments,
                                      'MIMES_AUDIO':MIMES_AUDIO,
                                      'MIMES_IMAGE':MIMES_IMAGE,
                                      'MIMES_FLASH':MIMES_FLASH})

# TODO: edition
@login_required
def submit(request, template="gallery/submit.html"):
    profile = request.user
    form = SubmissionForm()
    if request.POST:
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.profile = profile
            submission.file_mime = form.cleaned_data['file'].content_type
            submission.save()
            
            return redirect('gallery:view',
                            username=profile.username,
                            submission_id=submission.id)
        
    return render(request, template ,{'form':form,
                                      'profile':profile})