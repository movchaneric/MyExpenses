from django.urls import path
from . import views

urlpatterns = [
	#default route 
    path('', views.index, name = 'expenses'),
    path('add_expense/', views.add_expense, name = 'add_expense'),
    path('edit_expense/<str:id>/', views.edit, name='edit_expense'),
    path('delete_expense/<str:id>/', views.delete_expense, name='delete_expense')
    

]
