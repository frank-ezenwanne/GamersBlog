from django import forms
from django.forms import ModelForm
from .models import Post,Comment
# from django.core.files.storage import default_storage as storage
#from PIL import Image


class CreatePostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ['title','game_name','game_console','content','postimage']

	# def save(self,*args,**kwargs):
	# 	image_save = super(CreatePostForm,self).save(*args,**kwargs)
	# 	try:
	# 		img = Image.open(image_save.postimage)
	# 		if img.width >300 or img.height >300:
	# 			size=(300,300)
	# 			img.thumbnail(size)
	# 			fh = storage.open(image_save.postimage.name,"wb")
	# 			pic_format = "png"
	# 			img.save(fh,pic_format)
	# 			fh.close()
	# 			return image_save
	# 	except:
	# 		return image_save
		
			

	

class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ['comment_body','repliedcomid']

	def clean_comment_body(self):
		clean_comment_body = self.cleaned_data.get('comment_body')
		if clean_comment_body:
			if clean_comment_body == '*deleted-comment*':
				raise forms.ValidationError("Naa,You just can't type that..")
			return clean_comment_body


class PostUpdateForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title','game_name','game_console','content']


		