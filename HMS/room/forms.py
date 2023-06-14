from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from hotel.models import *


class editRoom(ModelForm):
    class Meta:
        model = Room
        fields = [
            "capacity",
            "numberOfBeds",
            "roomType",
            "price",
            "image",
            "description",
        ]


class editBooking(ModelForm):
    class Meta:
        model = Booking
        fields = ["startDate", "endDate"]


class editDependees(ModelForm):
    class Meta:
        model = Dependees
        fields = ["booking", "name"]
