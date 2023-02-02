from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Expense,Category
#import messages
from django.contrib import messages
from django.shortcuts import redirect
from .models import Expense

@login_required(login_url='authentication/login/')
def index(request):
	expenses = Expense.objects.filter(owner=request.user)
	categories = Category.objects.all()

	context = {'expenses':expenses}
	return render(request, 'expenses/index.html',context)


def add_expense(request):
	categories = Category.objects.all()

	if request.method == 'POST':
		amount = request.POST['amount']
		# user havent enter an amount
		if not amount:
			messages.error(request, 'Amount field is required')
		elif not amount.isnumeric():
			messages.error(request, 'Amount must contain only digits')
			return redirect('add_expense')
		elif float(amount) <= 0:
			messages.error(request, 'Amount has to be positive')

		description = request.POST['description']
		# Check if user updated description field
		if not description:
			messages.error(request, "Description field is required")
   
   
		category = request.POST['category']
		date = request.POST['date']

		# create the Expense in the db
		Expense.objects.create(owner=request.user, amount=amount, date=date, description=description, category=category)
		messages.success(request, "Expense created")
		return redirect('expenses')


	context = {'categories':categories}
	return render(request, 'expenses/add_expense.html',context)


def edit(request,id):
	# Get the expese data by expense id
	expense = Expense.objects.get(pk=id)
	categories = Category.objects.all()
 
	if request.method == 'GET':		
		context = {'expense':expense, 'values':expense, 'categories':categories}
		return render(request, 'expenses/edit_expense.html', context)

	if request.method == 'POST':
		amount = request.POST['amount']
		# check if user entered a new amount
		if not amount:
			messages.error(request, 'Amount field is required ')
   
		description = request.POST['description']
		# Check if user updated description field
		if not description:
			messages.error(request, "Description field is required")
   
   
		category = request.POST['category']
		date = request.POST['date']
  
		# update selected expense 
		expense.amount = amount
		expense.date = date
		expense.description = description
		expense.category = category

		# save an updated expense
		expense.save()
		
		# Show message succes to user
		messages.success(request, "Succesfuly updated expense")


		context = {'expense':expense, 'values':expense, 'categories':categories}
		return render(request, 'expenses/edit_expense.html', context)

# Delete expense
def delete_expense(request,id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Removed expense")
    return redirect('expenses')



