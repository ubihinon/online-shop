from django import forms
from django.contrib.auth.forms import UserCreationForm

from orders.models import Order
from users.models import User


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'first_name',
            'last_name',
            'patronymic',
            'region',
            'city',
            'postcode',
            'phone_number',
        )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required.', required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_exists = User.objects.filter(email=email).exists()
        if is_exists:
            raise forms.ValidationError("User already exists with this email")
        return email
