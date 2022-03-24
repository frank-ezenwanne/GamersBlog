from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField



class Profile(models.Model):
	image = ResizedImageField(size=[300,300],quality = 85 ,default = 'default.jpg',upload_to = 'profile_pics')
	user = models.OneToOneField(User, on_delete = models.CASCADE)


	def __str__(self):
		return f'{self.user.username} Profile'

	