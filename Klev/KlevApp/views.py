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

from KlevApp.ml.app_train_interface import *
from KlevApp.ml.train import *

import json
import requests
import time
# Create your views here.

# When training, the node expects the two-class model string,
# then the scaling parameters,
# then the 1-class model to be sent
# The end of each of those should be marked by an empty line (with \r),
# i.e. the last 4 characters sent should be \r\n\r\n
# Transaction should look like
# send "SENDING_MODEL\r\n"
# send two-class model string
# send "\r\n"
# send scaling-info
# send "\r\n"
# send one-class model string
# send "\r\n"
SENDING_TWO_CLASS_MODEL = "SENDING_TWO_CLASS_MODEL"
SENDING_SCALING_PARAMS = "SENDING_SCALING_PARAMS"
SENDING_ONE_CLASS_MODEL = "SENDING_ONE_CLASS_MODEL"

REQ_DATA_SUFFIX = "GET_DATA\r\n\0"
REQ_DATA_PREFIX = "#"
REQ_DATA_ITERS = 40

# Handling request for Home Page
def Index(request):
	context = {}
	return render(request, 'index.html', context)
# Handles request for initial call to add a device
# This is just the first page of the wizard, other pages are below
def AddDevice(request):
	context = {}
	context['AddDeviceForm'] = AddDeviceForm()
	return render(request, 'addDevice.html', context)

# Devices page
def Devices(request):
	context = {}
	devices = Device.objects.all()
	print("length devices")
	print(len(devices))
	for i in xrange(0,len(devices)):
		print(getattr(devices[i], 'deviceName'))
		print(getattr(devices[i], 'deviceState'))
		print(getattr(devices[i], 'trained'))
		print(getattr(devices[i], 'address') + "Equals the address the device is in")
		print(getattr(devices[i], 'city') + "Equals the city the device is in")
		print(getattr(devices[i], 'state') + "Equals the state the device is in")

	return render(request, 'devices.html', {'devices':devices})

def DeviceAdded(request):
	print(request)
	newDevice = Device(
                deviceName = request.POST.get('deviceName'),
                make = request.POST.get('make'),
                modelNum = request.POST.get('modelNum'),
                location = request.POST.get('location'),
                deviceState = "Untrained",
                photo = request.POST.get('photo'),
                state = request.POST.get('state'),
                address = request.POST.get('address'),
                city = request.POST.get('city'),
                zipCode = request.POST.get('zipCode'),)
	newDevice.save()
	return render(request, 'devices.html', {'devices':Device.objects.all()})



########
# View Functions for Training
########
"""
These functions are used to request and collect data lines from the node
"""
def send_data_req(rid):
        message = REQ_DATA_PREFIX + str(rid) + REQ_DATA_SUFFIX
        return
def get_data_line(rid):
        return "0.0 0.5 -0.3 0.76"
def get_device_data(nodeid, is_on, rid = [1]):
        data_file_name = get_data_file_name(nodeid)
        if (is_on):
                file_flags = 'a'
        else:
                file_flags = 'w'
        data_file = open(data_file_name, file_flags)
        for i in xrange(REQ_DATA_ITERS):
                this_rid = rid[0]
                rid[0] += 1
                dev_data = None
                while (dev_data == None):
                        send_data_req(this_rid)
                        time.sleep(0.1)
                        dev_data = get_data_line(this_rid)
                to_write = convert_line_to_libsvm_example(is_on, dev_data)
                to_write = to_write + "\n"
                data_file.write(to_write)
        data_file.close()
def generate_model_files(nodeid):
        data_file_name = get_data_file_name(nodeid)
	scale_and_train(data_file_name)
"""
These functions are used to send models back to the node
"""
def send_line(rid, message):
        while True:
                # send line over serial here
                time.sleep(0.1)
                # this should be something like
                # resp = get_ack(rid) that reads a serial line and
                # ensures the ack # matches rid
                resp = True
                if (resp):
                        return
def send_tc_model_req(rid):
        message = SENDING_TWO_CLASS_MODEL + str(rid) + "\r\n\0"
        send_line(rid, message)
        return
def send_file(fname, rid):
        f = open(fname, 'r')
        ids_used = 0
        for line in f:
                if (line[-1] == "\n"):
                        if (line[-2] == "\r"):
                                line = line + "\0"
                        else:
                                line = line[:-1] + "\r\n\0"
                elif (line[-1] == "\r"):
                        line = line + "\n\0"
                else:
                        line = line + "\r\n\0"
                message = "#" + str(rid) + "|" + line
                send_line(rid, message)
                rid += 1
                ids_used += 1
        f.close()
        message = "#" + str(rid) + "|" + "\r\n\0"
        send_line(rid, message)
        rid += 1
        return ids_used + 1
def send_scaling_req(rid):
        message = SENDING_SCALING_PARAMS + str(rid) + "\r\n\0"
        send_line(rid, message)
        return
def send_oc_model_req(rid):
        message = SENDING_ONE_CLASS_MODEL + str(rid) + "\r\n\0"
        send_line(rid, message)
        return
def send_models_to_node(nodeid, rid=[1]):
        dfn = get_data_file_name(nodeid)
        # send tc model
        tc_model_sent = False
        this_rid = rid[0]
        rid[0] += 1
        send_tc_model_req(this_rid)
        model = get_two_class_model_file_name(dfn)
        # this might be off by one for the rids
        rid[0] += send_file(model, this_rid+1)

        # send vector
        this_rid = rid[0]
        rid[0] += 1
        send_scaling_req(this_rid)
        scaling = get_scale_param_file_name(dfn)
        rid[0] += send_file(scaling, this_rid+1)

        # send oc model
        this_rid = rid[0]
        rid[0] += 1
        send_oc_model_req(this_rid)
        oc_model = get_one_class_model_file_name(dfn)
        rid[0] += send_file(oc_model, this_rid+1)

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

        # get data while the device is off
        get_device_data(device.nodeid, False)

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

        # get data while the device is on
        get_device_data(device.nodeid, True)

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

        # create models based on data we collected
        generate_model_files(device.nodeid)

        # send models to the node
        send_models_to_node(device.nodeid)

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

    return HttpResponse(response_text, content_type="application/json")


