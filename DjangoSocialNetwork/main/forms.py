from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=50, label = 'First name', required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=50, label = 'Last name', required=True, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, label = 'First name', required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=50, label = 'Last name', required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(max_length=50, label = 'Username', required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(max_length=50, label = 'Email', required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

class ProfileUpdateForm(forms.ModelForm):
    phone = forms.CharField(max_length=50, label = 'Phone', required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    address = forms.CharField(max_length=50, label = 'Address', required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'image']