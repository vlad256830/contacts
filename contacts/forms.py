from django import forms

from django.contrib.auth import get_user_model
from .models import Contact, Usersettings

User = get_user_model()


class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("Cannot use this email. It's already registered")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:            
            raise forms.ValidationError("Passwords don't match")
        return password2



class ContactForm(forms.ModelForm):
    first_name = forms.CharField(max_length=45)
    second_name = forms.CharField(max_length=45)
    town = forms.CharField(max_length=45)
    country = forms.CharField(max_length=45)
    telephone = forms.CharField(max_length=20)
    email = forms.CharField(max_length=45)
    date_of_birth = forms.DateField()
    

    class Meta:
        model = Contact
        fields = ('first_name', 'second_name', 'town','country','telephone','email','date_of_birth')
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        return first_name

    def clean_second_name(self):
        second_name = self.cleaned_data.get("second_name")
        return second_name

    def clean_town(self):
        town = self.cleaned_data.get("town")
        return town

    def clean_country(self):
        country = self.cleaned_data.get("country")
        return country
    
    def clean_telephone(self):
        telephone = self.cleaned_data.get("telephone")
        return telephone

    def clean_email(self):
        email = self.cleaned_data.get("email")
        return email

    def clean_date_of_birth(self):        
        date_of_birth = self.cleaned_data.get("date_of_birth")
        return date_of_birth

class UsersettingsForm(forms.ModelForm):      
    getvero_key = forms.CharField(max_length=255)
    getvero_username = forms.CharField(max_length=45)

    class Meta:
        model = Usersettings
        fields = ('getvero_key', 'getvero_username')

