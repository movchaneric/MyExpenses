from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Expense,Category
#import messages
from django.contrib import messages
from django.shortcuts import redirect

@login_required(login_url='authentication/login/')
def index(request):
	context = {}
	return render(request, 'expenses/index.html',context)

def add_expense(request):
	categories = Category.objects.all()

	if request.method == 'POST':
		amount = request.POST['amount']
		# user havent enter an amount
		if not amount:
			messages.error(request, 'Amount field is required ')
			# return render(request, 'expenses/add_expense.html',context)
		elif float(amount) <= 0:
			messages.error(request, 'Amount has to be positive ')


		description = request.POST['description']
		category = request.POST['category']
		date = request.POST['date']

		# create the Expense in the db
		Expense.objects.create(owner=request.user, amount=amount, date=date, description=description, category=category)
		messages.success(request, "Expense created")
		return redirect('expenses')


	context = {'categories':categories}
	return render(request, 'expenses/add_expense.html',context)
