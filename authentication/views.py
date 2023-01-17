from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib import auth

#import messages
from django.contrib import messages 

# Mail handle imports
from django.core.mail import EmailMessage
from django.core.mail import send_mail

from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

import json
from validate_email import validate_email
from .utils import email_verification_token

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

		# validate user data : username , email, password
		if not User.objects.filter(username=username).exists():
			if not User.objects.filter(email=email).exists():
				if len(password) < 3:
					print('Password is too short')
					return render(request, 'authentication/register.html', context)

				# user creation is validated
				user = User.objects.create_user(username=username, email=email, password=password)
				# deactivate user util email confirmation
				user.is_active = False
				user.save()
				
				# Email handle
				email_subject = 'Activate your account'

				# handle email verification link
				# get domain we are on
				domain = get_current_site(request).domain
				
				# get user id encrypted
				uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
				token = email_verification_token.make_token(user)

				link = reverse('activate', kwargs={'uidb64':uidb64, 'token':token})	

				# final activate_url concetinated
				activate_url = 'http://' + domain + link


				email_body = 'Hi ' + user.username + ' Please activate you account using the link belowe:\n' + activate_url 

				email = EmailMessage(
				    email_subject,
				    email_body,
				    'noreply@semycolon.com',
				    [email],
				)

				email.send(fail_silently = False)
				
				return render(request, 'expenses/index.html')


		return render(request, 'authentication/register.html')


# User verificaiton to activate user after registration
class VerificationView(View):
	def get(self, request, uidb64, token):

		# decode back user id 
		user_id = force_str(urlsafe_base64_decode(uidb64))

		# get user by id
		user = User.objects.get(pk = user_id)

		try:
			# decode back user id 
			user_id = force_str(urlsafe_base64_decode(uidb64))

			# get user by id
			user = User.objects.get(pk = user_id)

			# activate user and save
			user.is_active = True
			user.save()

			# check if user is already active 
			if user.is_active:
				print("User is already activated\n")
				return redirect('login')
		except Exception as e:
        		pass 

		return redirect('login')


class LoginView(View):
	def get(self, request):
		return render(request, 'authentication/login.html')

	def post(self, request):
		# get username and password
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			messages.success(request, user.username + " You are successfuly logged in")
			return render(request, 'expenses/index.html')
		else:
			messages.error(request, "Cradentials are invlaid try again")
			return render(request, 'authentication/login.html')

class LogoutView(View):
	def post(self, request):
		messages.success(request, request.user.username + " You are successfuly logged out")
		auth.logout(request)
		return render(request, 'authentication/logout.html')

















