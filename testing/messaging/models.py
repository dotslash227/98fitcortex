from django.db import models

# Create your models here.
class SMSTracking(models.Model):
	phone = models.CharField(max_length = 10 , db_index = True)
	message = models.CharField(max_length = 255)
	saved = models.DateTimeField(auto_now_add = True)
	source = models.CharField(null = True , max_length = 100)

	def __str__(self):
		return self.phone
