from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from profiles.models import Profile

    
class RegisterForm(forms.ModelForm):

    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
        'email_mismatch': _("The two email fields didn't match."),
        'duplicate_email': _("Address is already in use"),
    }
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))
    
    email1 = forms.EmailField(label=_('email'), required=True)
    email2 = forms.EmailField(label=_('verify email'), required=True)

    class Meta:
        model = Profile
        fields = ("username",)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            # Use iexact to check lower/uppercase
            Profile._default_manager.get(username__iexact=username)
        except Profile.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_email2(self):
        email1 = self.cleaned_data.get("email1")
        email2 = self.cleaned_data.get("email2")
        if email1 and email2 and email1 != email2:
            raise forms.ValidationError(
                self.error_messages['email_mismatch'],
                code='email_mismatch',
            )
        try:
            # Use iexact to check lower/uppercase
            Profile._default_manager.get(email=email2)
        except Profile.DoesNotExist:
            return email2
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def save(self, commit=True):
        profile = super(RegisterForm, self).save(commit=False)
        profile.set_password(self.cleaned_data["password1"])
        profile.email = self.cleaned_data["email1"]
        if commit:
            profile.save()
        return profile