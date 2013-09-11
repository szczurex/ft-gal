# Create your views here.
from django.template.loader import render_to_string
from messages.models import TaskedMail
from django.contrib.sites.models import get_current_site

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

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
    return render(request, template ,{'profile':profile})