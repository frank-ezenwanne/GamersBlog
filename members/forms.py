from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile
from django.core.files.storage import default_storage as storage
#from PIL import Image

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields=['username','email','password1','password2']



class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model =Profile
		fields = ['image']

	# def save(self,*args,**kwargs):
	# 	profile_save = super(ProfileUpdateForm,self).save(*args,**kwargs)
	# 	img = Image.open(profile_save.image)
	# 	if img.height > 300 or img.width > 300:
	# 		size =(300,300)
	# 		img.thumbnail(size)
	# 		fh = storage.open(profile_save.image.name,"wb")
	# 		pic_format = "png"
	# 		img.save(fh,pic_format)
	# 		fh.close()
	# 		return profile_save

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ['username','email']