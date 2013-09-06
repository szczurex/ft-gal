# Create your views here.
from django.template.loader import render_to_string


"""
    Need to think this whole thing through,
    either pass destination mail as a parameter
    OR a method to pull it out of the object.
    And what if there are multiple objects to pass?
"""

TEMPLATE_MAP = {
    'register_activate':{'template':'mail/activate.html',
                         'subject':'todo you are activated',
                         'mail_field':'TODO'}
}

def queue_message(msg_code, object):
    template = TEMPLATE_MAP.get(msg_code)
    
    if template:
        message = render_to_string(template, {'object':object})