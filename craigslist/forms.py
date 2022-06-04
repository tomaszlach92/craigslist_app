from django import forms
from craigslist.models import Announcement, Profile
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class AnnouncementForm(forms.ModelForm):
    """Form to add or update announcement."""
    class Meta:
        model = Announcement
        fields = ('title', 'description', 'price', 'category', 'image')
        labels = {
            'title': 'Tytuł ogłoszenia',
            'description': 'Opis',
            'price': 'Cena',
            'category': 'Kategoria',
            'image': 'Zdjęcie',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': "form-control col-md-6"}),
            'description': forms.Textarea(attrs={'class': "form-control"}),
            'price': forms.NumberInput(attrs={'class': "form-control"}),
            'category': forms.Select(attrs={'class': "form-control"}),
            'image': forms.FileInput(attrs={'class': "form-control"}),
        }


class LoginForm(forms.Form):
    """Form to log in user"""
    username = forms.CharField(label="Nazwa Użytkownika", widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput(attrs={'class': "form-control"}))


class RegisterUserForm(forms.ModelForm):
    """Form to register user"""
    repeat_password = forms.CharField(label="Powtórz hasło",
                                      widget=forms.PasswordInput(attrs={'class': "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'password',)
        labels = {
            'username': 'Nazwa Użytkownika',
            'password': 'Hasło'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': "form-control"}),
            'password': forms.PasswordInput(attrs={'class': "form-control"}),
        }

    def clean(self):
        """Compare the passwords that are the same"""
        cd = super().clean()
        password = cd['password']
        repeat_password = cd['repeat_password']
        if password != repeat_password:
            raise ValidationError("Podane hasła są różne")


class UserForm(forms.ModelForm):
    """Form to update user data"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'Adres Email',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "form-control"}),
            'last_name': forms.TextInput(attrs={'class': "form-control"}),
            'email': forms.EmailInput(attrs={'class': "form-control"}),
        }


class ProfileForm(forms.ModelForm):
    """Form to update profile data"""
    class Meta:
        model = Profile
        fields = ('street', 'zip_code', 'city', 'phone',)

        labels = {
            'city': 'Miasto',
            'street': 'Ulica',
            'zip_code': 'Kod Pocztowy',
            'phone': 'Numer telefonu',
        }
        widgets = {
            'city': forms.TextInput(attrs={'class': "form-control"}),
            'street': forms.TextInput(attrs={'class': "form-control"}),
            'zip_code': forms.TextInput(attrs={'class': "form-control"}),
            'phone': forms.EmailInput(attrs={'class': "form-control"}),
        }
