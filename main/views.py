from django.contrib import messages
from django.views.generic import ListView, DetailView,  CreateView, UpdateView, DeleteView
from .decorators import *
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.utils.decorators import method_decorator
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PasswordChangingForm, AddCommentForm
from .models import Profile, Post, Comment

# Create your views here.
@login_required
def home(request):
    context = {
        'posts': Post.objects.all().order_by('-date'),
        'comments': Comment.objects.all().order_by('-date')
    }
    return render(request, 'index.html', context)

class AddCommentView(LoginRequiredMixin, CreateView):
	model = Comment
	form_class = AddCommentForm
	template_name = 'main/add_comment.html'
	success_url = '/'

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.post_id = self.kwargs['pk']
		return super().form_valid(form)

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['body', 'img']
	success_url = '/'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['body', 'img']
	success_url = '/'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDetailView(DetailView):
	model = Post

	def get_context_data(self, **kwargs):
		context = super(PostDetailView, self).get_context_data(**kwargs)
		context['comments'] = Comment.objects.filter(post=self.object)
		return context

def other_profile(request, id=None):
	if id:
		other_user = Profile.objects.get(user_id=id)
		other_posts = Post.objects.filter(author_id=id).order_by('-date')
		post_list = []
		for x in other_posts:
			post_list.append(x)
	context = {
		'other_user': other_user,
		'other_posts' : post_list
		}
	return render(request, 'users/other_profiles.html', context)

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

class PasswordsChangeView(PasswordChangeView, LoginRequiredMixin):
	template_name = 'change-password.html'
	form_class = PasswordChangingForm
	success_url = 'profile'

@login_required
def profile(request):
	context = {
        'posts': Post.objects.filter(author=request.user).order_by('-date')
    }
	return render(request, 'profile.html', context)
	