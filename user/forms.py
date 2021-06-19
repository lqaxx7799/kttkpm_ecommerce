from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput, DateField, DateInput
from django.utils.translation import gettext as _

from home.models import UserProfile
class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30,label= 'User Name :')
    email = forms.EmailField(max_length=200,label= 'Email :')
    first_name = forms.CharField(max_length=100, help_text='First Name',label= 'First Name :')
    last_name = forms.CharField(max_length=100, help_text='Last Name',label= 'Last Name :')
    
    class Meta:
        model = User
        fields = ('username', 'email','first_name','last_name', 'password1', 'password2')


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ( 'username','email')
        widgets = {
            'username'  : TextInput(attrs={'class': 'input','placeholder':'username'}),
            'email'     : EmailInput(attrs={'class': 'input','placeholder':'email'}),
        }

GENDER = [
    ('Nam', 'Nam'),
    ('Nữ', 'Nữ'),
]
DATE_INPUT_FORMATS = ['%Y-%m-%d']
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        
        fields = ('hovaten', 'ngaysinh', 'gioitinh','diachi','sodt','image')

        widgets = {
            'hovaten'   : TextInput(attrs={'class': 'input','placeholder':'Họ và tên'}),
            'ngaysinh'  : forms.DateInput(attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'gioitinh'  : Select(attrs={'class': 'input','placeholder':'Giới tính'}, choices=GENDER),
            'diachi'    : TextInput(attrs={'class': 'input','placeholder':'Địa chỉ' }),
            'sodt'      : TextInput(attrs={'class': 'input','placeholder':'Số điện thoại'}),
            'image'     : FileInput(attrs={'class': 'input', 'placeholder': 'image',}),
        }


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Mật khẩu cũ"),widget=forms.PasswordInput)
    new_password1 = forms.CharField(label=_("Mật khẩu mới"),widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("Nhập lại mật khẩu"),widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': "Mật khẩu cũ"})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': "Mật khẩu mới"})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': "Nhập lại mật khẩu"})

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

