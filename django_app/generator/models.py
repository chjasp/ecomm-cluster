from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Token(models.Model):
	user_id = models.IntegerField(default=0)
	remaining_tokens = models.IntegerField(default=400)

	def __str__(self):
		return str(self.user_id)


