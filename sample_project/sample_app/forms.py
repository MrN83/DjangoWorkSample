from django import forms
from django.core import validators
from sample_app.models import WebUser, UserProfileInfo
from django.contrib.auth.models import User

#A way to implement custom validator
#Django expects the parameter "value"
#Use this later, e.g.: #name = forms.CharField(validators=[check_for_z])
def check_for_z(value):
    if value[0].lower() != 'z':
        raise forms.ValidationError("Name need to start with 'z'")

class FormName(forms.Form):
    #name = forms.CharField(validators=[check_for_z])
    name = forms.CharField()
    email = forms.EmailField()
    verify_email = forms.EmailField(label="Enter your email again:")
    text = forms.CharField(widget=forms.Textarea)
    #a bot would blindly add a value to this hidden input field
    #which helps identify that it is a bot
    botcatcher = forms.CharField(required=False,
                                widget=forms.HiddenInput,
                                validators=[validators.MaxLengthValidator(0)])

    #clean method - all such methods start with "clean_" and the name
    #of the field to be cleaned - Django's convention
    #This method will be run by Django to show an error message on the
    #form when validation fails.
    #Note: It is better to use built-in validators from django.core.
    #But this is better for more special cases.
    '''
    def clean_botcatcher(self):
        botcatcher = self.cleaned_data['botcatcher']

        if len(botcatcher) > 0:
            raise forms.ValidationError("GOTCHA BOT!")

        return botcatcher
    '''

    #Django convention: clean everything!
    def _clean(self):
        all_clean_data = super().clean() #return all clean data
        email = all_clean_data["email"]
        vmail = all_clean_data["verify_email"]

        if email != vmail:
            raise forms.ValidationError("Emails not matched.")

class FormWebUser(forms.ModelForm):
    #Can include the fields here or NOT (as they will be automatically
    #generated if fields = "__all__")
    class Meta:
        model = WebUser
        #ALSO OK: a tuple of some fields or exclude = [list of excluded field]
        fields = "__all__"


class FormUser(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class FormUserProfileInfo(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        exclude = ('user',) #everything except for the on-to-one user field
