from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from .forms import RegisterUserForm, EditProfileForm
from .decorators import *
from django.utils.decorators import method_decorator

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html', {})

# authentication
@user_passes_test(lambda user: not user.username, login_url='/', redirect_field_name=None)
def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			messages.success(request, ("There was an error logging into your account, please try again."))	
			return redirect('login')	
	else:
		return render(request, 'login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, ("Logged out successfully."))
	return redirect('/')

@user_passes_test(lambda user: not user.username, login_url='/', redirect_field_name=None)
def register_user(request):
	if request.method == 'POST':
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			form.save()
			username= form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Account registered successfully."))
			return redirect('/')
	else:
		form = RegisterUserForm()
	return render(request, 'register.html', {
		'form':form,
	})

# user
@login_required
def profile(request, username=None):
    return render(request, 'profile.html')

@method_decorator(login_required, name='dispatch')
class UserEditView(generic.UpdateView):
	form_class = EditProfileForm
	template_name = 'edit_profile.html'
	success_url = reverse_lazy('profile')

	def get_object(self):
		return self.request.user