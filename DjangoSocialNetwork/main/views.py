from django.contrib import messages
from django.views import generic
from .decorators import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile

# Create your views here.
class RedirectToPreviousMixin:

    default_redirect = '/'

    def get(self, request, *args, **kwargs):
        request.session[''] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['']

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
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username= form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Account registered successfully."))
			return redirect('/')
	else:
		form = UserRegisterForm()
	return render(request, 'register.html', {
		'form':form,
	})

# user
@login_required
def edit_profile(request):
	Profile.objects.get_or_create(user=request.user)
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, ("Your account has been updated."))
			return redirect('profile')
	else:	
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'u_form': u_form,
		'p_form': p_form
	}

	return render(request, 'edit_profile.html', context)

@login_required
def profile(request):
	return render(request, 'profile.html')


	