from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Expense(models.Model):
	amount = models.FloatField()
	date = models.DateField(default=now)
	description = models.TextField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.CharField(max_length=200)

	def __str__(self):
		return self.category

	# Order expenses by date 
	class Meta:
		ordering = ['-date']


class Category(models.Model):
	name = models.CharField(max_length=200)

	# Change name in the admin panel
	class Meta:
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.name
