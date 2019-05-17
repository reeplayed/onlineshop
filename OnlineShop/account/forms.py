from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class UserRegistration(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        all_emails = User.objects.all()
        emails = []
        for i in all_emails:
            emails.append(i.email)
        if email in emails:
            raise forms.ValidationError('Taki e-mail już istnieje')
        return email
