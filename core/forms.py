from django import forms
from .models import *

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        widgets = {
            "country": forms.TextInput(attrs={'class': 'form-control mt-1 mb-1 p-3'}),
            "first_name": forms.TextInput(attrs={'class': 'form-control mt-1 mb-1 p-3'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control mt-1 mb-1 p-3'}),
            "company_name": forms.TextInput(attrs={'class': 'form-control mt-1 mb-1 p-3'}),
            "Address": forms.TextInput(attrs={'class': 'form-control mt-1 mb-1 p-3'}),
            "city": forms.TextInput(attrs={'class': 'form-control mt-1 mb-1 p-3'}),
            "state": forms.TextInput(attrs={'class': 'form-control mt-1 mb-1 p-3'}),
            "zipcode": forms.TextInput(attrs={'class': 'form-control mt-1 mb-1 p-3'}),
            "email": forms.TextInput(attrs={'class': 'form-control mt-1 mb-1 p-3'}),
            "phone": forms.TextInput(attrs={'class': 'form-control mt-1 mb-1 p-3'}),
            
        }

class ShippingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = "__all__"
        widgets = {
            "shipping_country": forms.TextInput(attrs={'class': 'form-control mt-1 mb-1 p-3'}),
            "shipping_first_name": forms.TextInput(attrs={'class': 'form-control mt-1 mb-1 p-3'}),
            "shipping_last_name": forms.TextInput(attrs={'class': 'form-control mt-1 mb-1 p-3'}),
            "shipping_company_name": forms.TextInput(attrs={'class': 'form-control mt-1 mb-1 p-3'}),
            "shipping_Address": forms.TextInput(attrs={'class': 'form-control mt-1 mb-1 p-3'}),
            "shipping_city": forms.TextInput(attrs={'class': 'form-control mt-1 mb-1 p-3'}),
            "shipping_state": forms.TextInput(attrs={'class': 'form-control mt-1 mb-1 p-3'}),
            "shipping_zipcode": forms.TextInput(attrs={'class': 'form-control mt-1 mb-1 p-3'}),
            "shipping_email": forms.TextInput(attrs={'class': 'form-control mt-1 mb-1 p-3'}),
            "shipping_phone": forms.TextInput(attrs={'class': 'form-control mt-1 mb-1 p-3'}),
            
        }
