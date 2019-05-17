from django import forms
from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'town', 'street', 'postcode']

        def clean_postcode(self):
            post_code = self.cleaned_data.get("postcode")
            if '-' in post_code:
                raise forms.ValidationError('Wprowadź poprawny kod')
            return post_code