from django import forms

class CheckingForm(forms.Form):
    room_type = forms.CharField(max_length=50)
    check_in = forms.DateField(input_formats=["%D-%M-%Y"], error_messages={'required': "This field is required"})
    check_out = forms.DateField(input_formats=["%D-%M-%Y"], error_messages={'required': "This field is required"})