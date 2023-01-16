from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
	#default route 
    path('register/', views.RegisterView.as_view(), name = 'register'),
    path('login/', views.LoginView.as_view(), name = 'login'),
    path('user-validate/', csrf_exempt(views.UserNameValidation.as_view()), name = 'user_validate'),
    path('email-validate/', csrf_exempt(views.EmailValidation.as_view()), name = 'email_validate'),
    path('activate/<uidb64>/<token>/', csrf_exempt(views.VerificationView.as_view()), name = 'activate'),

]
