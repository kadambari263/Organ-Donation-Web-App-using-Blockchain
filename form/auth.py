from django import forms
from django.contrib.auth.forms import UserCreationForm
from home.model import HospitalProfile
from django.contrib.auth.models import User

# class RegisterForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     hospital_name = forms.CharField(max_length=255)
#     branch_name = forms.CharField(max_length=255)
#     address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Address'}))
#     mobile_number = forms.CharField(max_length=15)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
#         help_texts = {
#             'username': '',
#             'email': '',
#             'password1': '',
#             'password2': '',
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        
#         # Add placeholders to each field
#         self.fields['username'].widget.attrs['placeholder'] = 'Username'
#         self.fields['email'].widget.attrs['placeholder'] = 'Email'
#         self.fields['password1'].widget.attrs['placeholder'] = 'Password'
#         self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
#         self.fields['hospital_name'].widget.attrs['placeholder'] = 'Hospital Name'
#         self.fields['branch_name'].widget.attrs['placeholder'] = 'Branch Name'
#         self.fields['address'].widget.attrs['placeholder'] = 'Address'
#         self.fields['mobile_number'].widget.attrs['placeholder'] = 'Mobile Number'
        
#         # Remove help texts
#         for field_name in self.fields:
#             self.fields[field_name].help_text = ''

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    hospital_name = forms.CharField(max_length=255)
    branch_name = forms.CharField(max_length=255)
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    mobile_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': '',
            'email': '',
            'password1': '',
            'password2': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['hospital_name'].widget.attrs['placeholder'] = 'Hospital Name'
        self.fields['branch_name'].widget.attrs['placeholder'] = 'Branch Name'
        self.fields['address'].widget.attrs['placeholder'] = 'Address'
        self.fields['mobile_number'].widget.attrs['placeholder'] = 'Mobile Number'
        
        for field_name in self.fields:
            self.fields[field_name].help_text = ''

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            HospitalProfile.objects.create(
                user=user,
                hospital_name=self.cleaned_data['hospital_name'],
                branch_name=self.cleaned_data['branch_name'],
                address=self.cleaned_data['address'],
                mobile_number=self.cleaned_data['mobile_number'],
            )
        return user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
