from users.models import CustomUser
from django import forms

# class AdditionalSignUpInfoForm(forms.Form): # form to include firstname and lastname in django allauth
#     first_name = forms.CharField(max_length=30, label="First Name", required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
#     last_name = forms.CharField(max_length=30, label="Last Name", required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    
#     class Meta:
#         model = CustomUser
#     def save(self, user):
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.save()

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('image', 'first_name', 'last_name', 'country', 'age', 'occupation', 'birthday', 'mobile')


class UserSendEmailForm(forms.Form):
    recipient = forms.EmailField()
    subject = forms.CharField(max_length=50)
    message = forms.CharField(error_messages={'required': "This field is required"})