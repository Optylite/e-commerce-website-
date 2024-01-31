from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item, BillingDetails, ShippingOption
from django.contrib.auth.forms import PasswordChangeForm


class SignUp(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image')
        widgets = {
        'category': forms.Select(attrs={
            'class':'w-full py-4 px-6 rounded-xl border'
        }),
        'name': forms.TextInput(attrs={
            'class':'w-full py-4 px-6 rounded-xl border'
        }),
        'description': forms.Textarea(attrs={
            'class':'w-full py-4 px-6 rounded-xl border'
        }),
        'price': forms.TextInput(attrs={
            'class':'w-full py-4 px-6 rounded-xl border'
        }),
        'image': forms.FileInput(attrs={
            'class':'w-full py-4 px-6 rounded-xl border'
        })
    }
        
class DetailsForm(forms.ModelForm):
    class Meta:
        model = BillingDetails
        fields = '__all__'

class OrderForm(forms.Form):
    shipping_option = forms.ModelChoiceField(queryset=ShippingOption.objects.all(), empty_label=None)
    

class UserForm(forms.ModelForm):
    model = User
    fields = ['username']

class EditDetailForm(forms.ModelForm):
    class Meta:
        model = BillingDetails
        fields = ['user','company', 'firstname', 'lastname', 'phone_number', 'email']

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User 