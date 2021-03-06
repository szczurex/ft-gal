from django import forms
from gallery.models import Submission, Submission_Comment

# TODO: file verification
from gallery.validators import THUMB_VALIDATOR, FILE_VALIDATOR


class SubmissionForm(forms.ModelForm):
    
    class Meta:
        model = Submission
        exclude = ('profile', 'date_created', 'date_edited', 'deleted', 'file_mime')
        widgets={'description': forms.Textarea}
    
    def __init__(self, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
        self.fields['file'].validators = [FILE_VALIDATOR]
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Submission_Comment
        exclude = ('profile', 'comment', 'date_created', 'deleted', 'submission')
        widgets={'content': forms.Textarea}