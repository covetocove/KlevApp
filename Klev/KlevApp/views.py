from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse, Http404
from django.core import serializers

from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from mimetypes import guess_type
from KlevApp.models import *
from KlevApp.forms import *
import json
import requests
# Create your views here.


def index(request):
	context = {}
	return render(request, 'index.html', context)

def addDevice(request):
	context = {}
	context['AddDeviceForm'] = AddDeviceForm()
	return render(request, 'addDevice.html', context)

def devices(request):
	context = {}
	return render(request, 'devices.html', {'devices':Device.objects.all()})

def deviceAdded(request):
	print(request)
	newDevice = Device(deviceName = request.POST.get('deviceName'),
	make = request.POST.get('make'), modelNum = request.POST.get('modelNum'),
	location = request.POST.get('location'), deviceState = "Untrained",
	photo = request.POST.get('photo'),)
	newDevice.save()
	return render(request, 'devices.html', {'devices':Device.objects.all()})