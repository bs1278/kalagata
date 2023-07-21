from django.db import models

# Create your models here.

class BaseClass(models.Model):
	name = models.CharField(max_length=88)
	created = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Toll(BaseClass):

	def __str__(self):
		return self.name


class TollBooth(BaseClass):
	toll = models.ForeignKey(Toll, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.name


class Vehicle(models.Model):
	registration_num = models.CharField(max_length=88,unique=True)

	def __str__(self):
		return self.registration_num


class TollPass(models.Model):
	SP = 'S'
	RP = 'R'
	SDP = '7D'

	PASS_TYPES = (
		(SP, 'Single Pass'),
		(RP, 'Return Pass'),
		(SDP, '7 Day pass'),

	)

	pass_type = models.CharField(max_length=2, choices=PASS_TYPES)
	vehicle = models.ForeignKey(Vehicle,on_delete=models.CASCADE)
	valid_from = models.DateTimeField()
	valid_untill = models.DateTimeField()


class TollTransaction(models.Model):
	toll_booth = models.ForeignKey(TollBooth, on_delete=models.CASCADE)
	vehicle = models.ForeignKey(Vehicle,on_delete=models.CASCADE)
	toll_pass = models.ForeignKey(TollPass,on_delete=models.CASCADE,null=True)
	transaction_time = models.DateTimeField(auto_now_add=True)
	amt_collected = models.DecimalField(max_digits=10,decimal_places=2)