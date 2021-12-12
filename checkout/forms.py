from django import forms
from localflavor.us.forms import USStateSelect, USZipCodeField
from .models import Order
from profiles.models import UserProfile


class OrderForm(forms.ModelForm):
    ship_zipcode = USZipCodeField()
    bill_zipcode = USZipCodeField()
    """ Widget code from Nafees Anwar on stackoverflow 4/30/19 """
    ship_state = forms.CharField(widget=USStateSelect)
    bill_state = forms.CharField(widget=USStateSelect)
    marketing = forms.BooleanField(widget=forms.CheckboxInput, required=False)

    class Meta:
        model = UserProfile
        field = ('marketing',)

        model = Order
        fields = (
            'ship_full_name', 'email', 'ship_comp_name',
            'ship_phone_number', 'ship_street_address1',
            'ship_street_address2', 'ship_city', 'ship_state',
            'ship_zipcode', 'bill_full_name', 'bill_phone_number',
            'bill_street_address1', 'bill_street_address2',
            'bill_city', 'bill_state', 'bill_zipcode',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'ship_full_name': 'Full Name',
            'ship_comp_name': 'Organization',
            'email': 'Email Address',
            'ship_phone_number': 'Phone',
            'ship_street_address1': 'Street Address 1',
            'ship_street_address2': 'Street Address 2',
            'ship_city': 'City',
            'ship_state': 'State',
            'ship_zipcode': 'Zip Code',
            'bill_full_name': 'Full Name',
            'bill_phone_number': 'Phone',
            'bill_street_address1': 'Street Address 1',
            'bill_street_address2': 'Street Address 2',
            'bill_city': 'City',
            'bill_state': 'State',
            'bill_zipcode': 'Zip Code',
            'marketing': "",
        }

        self.fields['email'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
            self.fields['marketing'].widget.attrs['class'] = 'form-check-input'


class ShippingForm(forms.ModelForm):
    ship_zipcode = USZipCodeField()
    """ Widget code from Nafees Anwar on stackoverflow 4/30/19 """
    ship_state = forms.CharField(widget=USStateSelect)
    marketing = forms.BooleanField(widget=forms.CheckboxInput, required=False)

    class Meta:
        model = UserProfile
        field = ('marketing',)

        model = Order
        fields = (
            'ship_full_name', 'email', 'ship_comp_name',
            'ship_phone_number', 'ship_street_address1',
            'ship_street_address2', 'ship_city', 'ship_state',
            'ship_zipcode',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'ship_full_name': 'Full Name',
            'ship_comp_name': 'Organization',
            'email': 'Email Address',
            'ship_phone_number': 'Phone',
            'ship_street_address1': 'Street Address 1',
            'ship_street_address2': 'Street Address 2',
            'ship_city': 'City',
            'ship_state': 'State',
            'ship_zipcode': 'Zip Code',
            'marketing': "",
        }

        self.fields['email'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False
            self.fields['marketing'].widget.attrs['class'] = 'form-check-input'