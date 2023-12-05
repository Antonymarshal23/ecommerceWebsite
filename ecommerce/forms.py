from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Customer

class CostomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', ]



class CreateUserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # def __init__(self, *args, **kwargs):
    #     super(CreateUserForm, self).__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter username'})
    #     self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})
    #     self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})