from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages

import json

from validate_email import validate_email

# Create your views here.
class UserNameValidation(View):

	def post(self, request):

		data = json.loads(request.body)
		username = data['username']

		# Check if username contains not alphanumeric characters
		if not str(username).isalnum():
			return JsonResponse({'username_error': 'Username should only contain alphanumerics'})

		# Check if username already exists
		if User.objects.filter(username = username).exists():
			return JsonResponse({'username_error': 'Username is already exists'})


		return JsonResponse({'Username': True})

class EmailValidation(View):

	def post(self, request):

		data = json.loads(request.body)
		email = data['email']

		# check mail validation 
		if not validate_email(email):
			return JsonResponse({'email_error':'Email is not in the right format'})

		if User.objects.filter(email=email).exists():
			return JsonResponse({'email_error': 'Email already exists'})

		return JsonResponse({'email': True})


class RegisterView(View):
	# handle get request
	def get(self, request):
		return render(request, 'authentication/register.html')

	def post(self, request):
		# get user data
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']

		context = { 'fieldValues': request.POST }

		# valida3te user data : username , email, password
		if not User.objects.filter(username=username).exists():
			if not User.objects.filter(email=email).exists():
				if len(password) < 3:
					print('Password is too short')
					return render(request, 'authentication/register.html', context)

				# user creation is validated
				user = User.objects.create_user(username=username, email=email, password=password)
				# save user
				user.save()
				return render(request, 'expenses/index.html')


		return render(request, 'authentication/register.html')
















