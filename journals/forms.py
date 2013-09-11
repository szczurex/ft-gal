from django import forms
from journals.models import Journal


class JournalForm(forms.ModelForm):
    
    class Meta:
        model = Journal
        exclude = ('profile', 'date_created', 'date_edited', 'deleted')
        widgets={'content': forms.Textarea}