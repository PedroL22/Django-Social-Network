from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    first_name = forms.CharField(max_length=50, label = 'First name', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First name'}))
    last_name = forms.CharField(max_length=50, label = 'Last name', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last name'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, label = 'First name', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First name'}))
    last_name = forms.CharField(max_length=50, label = 'Last name', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last name'}))
    username = forms.CharField(max_length=50, label = 'Username', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    email = forms.EmailField(max_length=50, label = 'Email', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

class ProfileUpdateForm(forms.ModelForm):
    phone = forms.CharField(max_length=50, label = 'Phone', required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}))
    address = forms.CharField(max_length=50, label = 'Address', required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}))
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['bio'].required = False

    class Meta:
        model = Profile
        fields = ['phone', 'address', 'bio', 'image']
        widgets = {
            'bio': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Bio'}),
        }

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, label = 'Old password', required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password1 = forms.CharField(max_length=50, label = 'New password', required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password2 = forms.CharField(max_length=50, label = 'New password confirmation', required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
        