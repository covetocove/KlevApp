from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from models import *


class AddDeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        exclude = ('trained', 'deviceState', 'deviceid',)
        widgets = {'photo' : forms.FileInput(), }
