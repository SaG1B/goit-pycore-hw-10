from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш Email'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ім\'я користувача'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Користувач з такою електронною поштою вже існує.")
        return email