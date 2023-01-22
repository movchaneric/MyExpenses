from django.shortcuts import render
import json
import os
from django.conf import settings
from .models import UserPreferece
#import messages
from django.contrib import messages 

# Create your views here.
def index(request):
	currencies_arr = []
	# get path of the file
	path = os.path.join(settings.BASE_DIR, 'currencies.json')
	# open file with read mode and load it as alist of dictioanry
	with open(path, 'r') as json_file:
		data = json.load(json_file)

		for key,value in data.items():
			currencies_arr.append({'name':key, 'value':value})

	# get user_preferce by user logged in
	user_preferece = None

	# Check if user already exists
	if UserPreferece.objects.filter(user=request.user).exists():
		user_preferece = UserPreferece.objects.get(user=request.user)

	if request.method == "GET":

		context = {'currencies_arr':currencies_arr, 'user_preferece':user_preferece}

		return render(request, 'userpreferences/index.html', context)

	# POST METHOD
	else:
		selected_currency = request.POST['currency']

		if UserPreferece.objects.filter(user=request.user).exists():
			
			#set user currency to selected choice
			user_preferece.currency = selected_currency

			# save
			user_preferece.save()
		else:

			UserPreferece.objects.create(user=request.user, currency=selected_currency)

		# show message to show selected currency
		messages.success(request, "Change currency to: " + selected_currency)

		context = {'currencies_arr':currencies_arr ,'user_preferece':user_preferece}

		return render(request, 'userpreferences/index.html', context)
