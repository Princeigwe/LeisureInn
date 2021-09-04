from django import forms
from django.db.models.base import Model
from bootstrap_datepicker_plus import DatePickerInput
from .models import Booking

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


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guest_firstname', 'guest_lastname', 'guest_email', 'guest_telephone', 'amount']