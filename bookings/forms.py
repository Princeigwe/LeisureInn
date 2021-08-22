from django import forms
from bootstrap_datepicker_plus import DatePickerInput

ROOM_OPTIONS = (
    ('SINGLE ROOM', 'Single Room'),
    ('DOUBLE ROOM', 'Double Room'),
    ('TRIPLE ROOM', 'Triple Room'),
    ('QUAD ROOM', 'Quad Room'),
)

class CheckingForm(forms.Form):
    room_type = forms.ChoiceField(choices=ROOM_OPTIONS, widget=forms.Select)
    check_in = forms.DateField(widget=DatePickerInput(format='%m/%d/%Y'), error_messages={'required': "This field is required"})
    check_out = forms.DateField(widget=DatePickerInput(format='%m/%d/%Y'), error_messages={'required': "This field is required"})
