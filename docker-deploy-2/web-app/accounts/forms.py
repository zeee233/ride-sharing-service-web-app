from django import forms
from ridesharing.models import Driver
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['vehicle_type', 'license_plate_number', 'max_passengers','special_vehicle_info']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email','password1','password2')