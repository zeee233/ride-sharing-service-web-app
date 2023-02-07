from django import forms
from ridesharing.models import RideSharer,RideOwner
class RideSharerForm(forms.ModelForm):
    class Meta:
        model = RideSharer
        fields = ['destination', 'earliest_arrival', 'latest_arrival', 'number_passengers']

class EditOwnerForm(forms.ModelForm):
    class Meta:
        model = RideOwner
        fields = ['destination', 'arrival_date_time', 'number_requested', 'vehicle_type', 'special_requests']
class RideDropForm(forms.ModelForm):
    drop_ride = forms.BooleanField(required=False)
    class Meta:
        model = RideSharer
        fields = ['number_passengers', 'drop_ride']

