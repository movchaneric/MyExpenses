from django.urls import path
from . import views

urlpatterns = [
	#default route 
    path('', views.index, name = 'expenses'),
    path('add_expense/', views.add_expense, name = 'add_expense'),

]
