from django import forms
from django.contrib.auth.forms import AuthenticationForm ,UsernameField ,UserCreationForm ,PasswordChangeForm
from .models import User

class LoginForm(AuthenticationForm):
    password = forms.CharField(label_suffix='', widget=forms.PasswordInput(attrs={'class':'auth-password ','placeholder':'Password','autofocus':False}))
    username = UsernameField(label_suffix='',widget=forms.TextInput(attrs={'class':'auth-username','placeholder':'Email or Mobile'}))



class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(label_suffix='',widget=forms.PasswordInput(attrs={'class':'auth-password','placeholder':'Password', 'id':'password1' }))
    password2 = forms.CharField(label_suffix='',widget=forms.PasswordInput(attrs={'class':'auth-password','placeholder':'confirm Password','id':'password2'}))
    username = UsernameField(label_suffix='',widget=forms.TextInput(attrs={'class':'auth-username','placeholder':'Username','autofocus':'off','id':'username'}))
    email = forms.CharField(label_suffix='',widget=forms.EmailInput(attrs={'class':'auth-password','placeholder':'Email','id':'email-update'}))
    
    class Meta:
        model = User
        fields =['username','email']
    
class UserChangePassword(PasswordChangeForm):
    old_password = forms.CharField(label_suffix='',widget=forms.PasswordInput(attrs={'class':'password-form','placeholder':'Current password'}))
    new_password1 = forms.CharField(label_suffix='',widget=forms.PasswordInput(attrs={'class':'password-form','placeholder':'New password'}))
    new_password2 = forms.CharField(label_suffix='',widget=forms.PasswordInput(attrs={'class':'password-form','placeholder':'Comfirm '}))


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['mobile','username','profile_image']
        widgets = {
            'profile_image':forms.FileInput(attrs={'class':'form-control'}),
        }
