from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm
from .forms import UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data["username"]
			messages.success(request, f' Your account has been successfully created..You can now login')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request,'members/register.html',{'form':form})

	



@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST,instance = request.user)
		p_form = ProfileUpdateForm(request.POST,request.FILES,instance = request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, "Profile has been updated")
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance = request.user)
		p_form = ProfileUpdateForm(instance = request.user.profile)

	context = {"u_form":u_form,
				"p_form": p_form}

	return render(request, 'members/profile.html',context)


@login_required
def DeleteAccountView(request):
	return render(request,"members/account_confirm_delete.html")

@login_required
def ConfirmAccDeleteView(request):
	get_user = get_object_or_404(User,id = request.user.id)
	get_user.delete()
	return redirect('post-list')

