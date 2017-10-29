from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username", max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'name': 'username'}
        ))
    password = forms.CharField(
        label="Password", max_length=30,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'name': 'password'}
        ))


class SignUPForm(forms.Form):
    username = forms.CharField(
        label="Username", max_length=30, widget=forms.TextInput(attrs={
            'class': 'form-control one-liner-username', 'name': 'username'}))
    name = forms.CharField(
        label="Full Name", max_length=30, widget=forms.TextInput(
            attrs={'class': 'form-control one-liner-name', 'name': 'name'}))
    phone = forms.CharField(
        label="Phone no", max_length=10, min_length=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control one-liner', 'name': 'phone'}))
    password = forms.CharField(
        label="Password", max_length=30, widget=forms.PasswordInput(
            attrs={'class': 'form-control one-liner', 'name': 'password'}))
    email = forms.EmailField(
        label="Email", max_length=30, widget=forms.EmailInput(
            attrs={'class': 'form-control one-liner-email', 'name': 'email'}))
    COUNTRY_CHOICES = (
        ("choose country", "Select"), ("india", "INDIA"),
        ("pakistan", "PAKISTAN"), ("bangaldesh", "BANGLADESH"),
        ("srilanka", "SRILANKA"), ("unitedstates", "US"), ("nepal", "NEPAL"),
        ("australia", "AUSTRALIA"))
    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES, label='Country', required=True,
        widget=forms.Select(attrs={
            'class': 'form-control one-liner-country', 'name': 'country'}
        ))
    terms = forms.BooleanField(
        label="Terms & Conditions", widget=forms.CheckboxInput(
            attrs={'class': 'forms-control one-liner-terms', 'name': 'terms'}))


class ProfileForm(forms.Form):
    """Build profile for registered users"""
    alternate_phone_no = forms.CharField(required=False)
    std_code = forms.IntegerField(required=False)
    alternate_email = forms.EmailField(required=False)
    pincode = forms.CharField(required=False, max_length=10)
    address = forms.CharField(required=False, max_length=125)
    hobbies = forms.CharField(required=False, max_length=32)


class Academic(forms.Form):
    year_of_passing = forms.DateField()
    percentage = forms.FloatField()
    institute = forms.CharField(max_length=256)
    location = forms.CharField(max_length=64)
