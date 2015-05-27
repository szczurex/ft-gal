# Create your views here.
from django.template.loader import render_to_string
from msg.models import TaskedMail
from django.contrib.sites.models import get_current_site
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.contenttypes.models import ContentType
from msg.models import Notification
from profiles.models import ProfileWatch
from journals.models import Journal
from gallery.models import Submission, Submission_Comment
from favourites.models import Favourite
from gallery.validators import MIMES_AUDIO, MIMES_IMAGE, MIMES_FLASH
"""
    Need to think this whole thing through,
    either pass destination mail as a parameter
    OR a method to pull it out of the object.
    And what if there are multiple objects to pass?
"""

TEMPLATE_MAP = {
    'register_activate':{'template':'mail/activate.html',
                         'subject':'Your activation link'}
}

"""
    Return True or False, depending on success of queue
"""
def queue_message(request, msg_code, object, email):
    code = TEMPLATE_MAP.get(msg_code)
    
    if code:
        current_site    = get_current_site(request)
        site_name       = current_site.name
        domain          = current_site.domain
        
        mail_dict = {
            'domain':domain,
            'site_name':site_name,
            'protocol':request.is_secure() and 'https' or 'http',
            'object':object,
        }
        
        message = render_to_string(code['template'], mail_dict)
        
        mail                = TaskedMail()
        mail.subject        = code['subject']
        mail.destination    = email
        mail.message        = message
        
        mail.save()
        
        return True
    
    return False


@login_required
def index(request, template="messages/index.html"):
    profile = request.user
    
    ct_watch = ContentType.objects.get_for_model(ProfileWatch)
    ct_submission = ContentType.objects.get_for_model(Submission)
    ct_journal = ContentType.objects.get_for_model(Journal)
    ct_favourite = ContentType.objects.get_for_model(Favourite)
    ct_sub_comment = ContentType.objects.get_for_model(Submission_Comment)
    
    
    nf_watches = Notification.objects.filter(content_type=ct_watch, profile=profile)
    nf_submissions = Notification.objects.filter(content_type=ct_submission, profile=profile)
    nf_journals = Notification.objects.filter(content_type=ct_journal, profile=profile)
    nf_favourites = Notification.objects.filter(content_type=ct_favourite, profile=profile)
    nf_sub_comments = Notification.objects.filter(content_type=ct_sub_comment, profile=profile)
    
    if request.POST:
        removable_ids = request.POST.getlist('remove')
        if removable_ids:
            notifs = Notification.objects.filter(id__in = removable_ids,
                                                 profile = request.user)
            if notifs:
                notifs.delete()
                return redirect('messages:index')
        
    return render(request, template ,{'profile':profile,
                                      'nf_watches':nf_watches,
                                      'nf_submissions':nf_submissions,
                                      'nf_journals':nf_journals,
                                      'nf_favourites':nf_favourites,
                                      'nf_sub_comments':nf_sub_comments,
                                      'MIMES_AUDIO':MIMES_AUDIO,
                                      'MIMES_IMAGE':MIMES_IMAGE,
                                      'MIMES_FLASH':MIMES_FLASH})

