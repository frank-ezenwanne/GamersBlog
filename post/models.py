from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.core.files.storage import default_storage as storage
from django_resized import ResizedImageField

def get_deleted_user_instance():
	return User.objects.get(username = 'deleted-user')

class Post(models.Model):
	title = models.CharField(max_length = 115)
	slug = models.SlugField(null=True) #REMOVE NULL LATER
	content = models.TextField(blank = True, null = True)
	game_console = models.CharField(max_length = 20,null = True,blank = True)
	game_name = models.CharField(max_length = 100,null = True,blank = True)
	date_posted = models.DateTimeField(default = timezone.now)
	author = models.ForeignKey(User, on_delete = models.SET(get_deleted_user_instance))
	postimage = ResizedImageField(size=[300,300],quality = 85, blank = True, null = True,upload_to = "post_images")
	likes = models.ManyToManyField(User, related_name = "postlikefield")
	
	def __str__(self):
		return self.title

	def save(self,*args,**kwargs):
		if not self.slug:
			super().save(*args,**kwargs)
			slug = slugify(self.title)
			pk = str(self.pk * 2)
			#if self.__class__.objects.filter(author=self.author).filter(slug__in = [slug]).exists():#if the slug created already exists,add an id
			slug = slug + pk
			self.slug = slug

		return super().save(*args,**kwargs)
		



	def get_absolute_url(self):
		return reverse('post-detail',kwargs ={'username':self.author.username,"slug":self.slug})


class Comment(models.Model):
	post = models.ForeignKey(Post,on_delete = models.CASCADE)
	commenter = models.ForeignKey(User,on_delete=models.SET(get_deleted_user_instance))
	date_posted = models.DateTimeField(default = timezone.now)
	comment_body = models.TextField()
	repliedcomid = models.ForeignKey('self', related_name = 'repcom', on_delete = models.DO_NOTHING,blank=True,null = True)
	likes = models.ManyToManyField(User,related_name = 'commentlikefield')
	def __str__(self):
		return f"{self.commenter.username}'s comment"

