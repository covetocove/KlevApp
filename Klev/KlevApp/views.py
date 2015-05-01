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

from KlevApp.ml.app_train_interface import train_state


import json
import requests
# Create your views here.


def Index(request):
	context = {}
	return render(request, 'index.html', context)

def AddDevice(request):
	context = {}
	context['AddDeviceForm'] = AddDeviceForm()
	return render(request, 'addDevice.html', context)

def Devices(request):
	context = {}
	devices = Device.objects.all()
	print("length devices")
	print(len(devices))
	for i in xrange(0,len(devices)):
		print(getattr(devices[i], 'deviceName'))
		print(getattr(devices[i], 'deviceState'))
		print(getattr(devices[i], 'trained'))
	return render(request, 'devices.html', {'devices':devices})

def DeviceAdded(request):
	print(request)
	newDevice = Device(deviceName = request.POST.get('deviceName'),
	make = request.POST.get('make'), modelNum = request.POST.get('modelNum'),
	location = request.POST.get('location'), deviceState = "Untrained",
	photo = request.POST.get('photo'),)
	newDevice.save()
	return render(request, 'devices.html', {'devices':Device.objects.all()})



########
# View Functions for Training
########
def TrainDevice(request):
	# Gets device from objects
	## TODO: need to better filter that you're getting the correct device
	print(request.POST)
	device = Device.objects.all().get(deviceName= request.POST.get('Device'))
	print(device)
	context = {}
	return render(request, 'trainDevice.html', {'device':device})

## Device now in the off state, training should start
def TrainOff(request):
	# Gets device from objects
	## TODO: need to better filter that you're getting the correct device
	print(request.POST)
	device = Device.objects.all().get(deviceName= request.POST.get('Device'))
	print(device)
	context = {}
	train_state(device.deviceName, False)
	return render(request, 'finishOff.html', {'device':device})


## User has now manually ended 'off' training at the end of 5 minutes
# ML should stop 'off' training and get ready for user to turn on Device for on training
def FinishOff(request):
	# Gets device from objects
	## TODO: need to better filter that you're getting the correct device
	print(request.POST)
	device = Device.objects.all().get(deviceName= request.POST.get('Device'))
	print(device)
	context = {}
	return render(request, 'trainOn.html', {'device':device})


def TrainOn(request):
	# Gets device from objects
	## TODO: need to better filter that you're getting the correct device
	print(request.POST)
	device = Device.objects.all().get(deviceName= request.POST.get('Device'))
	print(device)
	context = {}
	train_state(device.deviceName, True)
	return render(request, 'finishOn.html', {'device':device})

# User has now manually ended 'on' training at the end of 5 minutes
# ML should stop 'on' training and return to devices
def FinishOn(request):
	# Gets device from objects
	## TODO: need to better filter that you're getting the correct device
	print(request.POST)
	device = Device.objects.all().get(deviceName= request.POST.get('Device'))
	print(device)
	context = {}
	return render(request, 'finishTrainOff.html', {'device':device})

def TrainingFinished(request):
	# Gets device from objects
	## TODO: need to better filter that you're getting the correct device
	print(request.POST)
	device = Device.objects.all().get(deviceName= request.POST.get('Device'))
	print(device)
	# TODO: update device state based on ML: 
	# device['deviceState'] = # Code that uses ML to test device state
	setattr(device, 'deviceState', 'field value')
	setattr(device, 'trained', 1)
	context = {}
	print(device)
	print("device data:")
	print("deviceName")
	print(getattr(device, 'deviceName'))
	print("state")

	print(getattr(device, 'deviceState'))
	print("trained")

	print(getattr(device, 'trained'))
	device.save()
	return render(request, 'devices.html', {'devices':Device.objects.all()})

def Get_Devices(request):
    response_text = serializers.serialize("json", Device.objects.all())
    print("JSON Response = ", response_text)
    print("HEEEEEEEEEEEEE\nEeeeeeeeen\neeeeeeellll\nlllllllooo\noooooooooooooooo")

    return HttpResponse(response_text, content_type="application/json")


