from django.db import models

# Create your models here.

class Analysis(models.Model):
	text = models.CharField(max_length=100000)
	heading = models.CharField(max_length=10000)
	source = models.CharField(max_length=1000)
	author = models.CharField(max_length=10000)
	label = models.IntegerField(default=-1)

	pants_on_fire = models.FloatField(default=0.00) 
	false = models.FloatField(default=0.00)
	barely_true = models.FloatField(default=0.00)
	half_true = models.FloatField(default=0.00)
	mostly_true = models.FloatField(default=0.00)
	true = models.FloatField(default=0.00)
