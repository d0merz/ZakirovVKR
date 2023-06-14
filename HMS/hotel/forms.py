from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import *


class createEventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            "eventType",
            "location",
            "startDate",
            "endDate",
            "explanation",
        ]


class editEvent(ModelForm):
    class Meta:
        model = Event
        fields = [
            "eventType",
            "location",
            "startDate",
            "endDate",
            "explanation",
        ]
