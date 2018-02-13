from django.contrib.auth.models import User, Group
from django import forms
from django.core.exceptions import ValidationError
from accounts.models import *
from django.contrib.auth.forms import UserChangeForm


from organizer.forms import NewSlotForm

"""class EditProfileForm(forms.Form):
    bio = forms.CharField(label='Bio', max_length=960, widget=forms.TextInput(
        attrs={
            'type': 'text',
            'class': 'form',
            'value': profile.bio
            }))

    def clean_bio(self):
        bio = self.cleaned_data['bio']
        return bio

    def save(self, commit=True):
        try:

            profile = Profile(
            objects=object,
            timezone=timezone,
            team=team,
            username=username,
            bio=self.cleaned_data['bio'],
            hours=hours
            )
            return profile
        except Exception as e:
            raise"""


class EditProfileForm(forms.Form):




    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile', None)
        super(EditProfileForm, self).__init__(*args, **kwargs)

    bio = forms.CharField(label='Bio', max_length=360, widget=forms.Textarea(
        attrs={
            'type': 'text',
            'class': 'form-control',
            'rows': 5,
            'style': 'resize:none;',
        }))

    def clean_bio(self):
        bio = self.cleaned_data['bio']
        return bio

    def save(self, commit=True):
        return self.cleaned_data['bio']


class EditUserForm(UserChangeForm):
    template_name = '/accounts/editProfile'
    first_name = forms.CharField(label='First Name', max_length=150, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', max_length=150, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    username = forms.CharField(label='Username', min_length=4, max_length=150, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    email = forms.EmailField(label='Email', max_length=200, widget=forms.EmailInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'username',
            'password',
        )



# The form for user signups
class SignupForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=150, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', max_length=150, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    username = forms.CharField(label='Username', min_length=4, max_length=150, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    email = forms.EmailField(label='Email', max_length=200, widget=forms.EmailInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'type': 'text',
               'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'type': 'text',
               'class': 'form-control'}))

    # May only contain alphabetical characters
    def clean_firstname(self):
        first_name = self.cleaned_data['first_name'].title()
        if not first_name.isalpha():
            raise ValidationError("You name must contain only letters")
        return first_name

    # May only contain alphabetical characters
    def clean_lastname(self):
        last_name = self.cleaned_data['last_name'].title()
        if not last_name.isalpha():
            raise ValidationError("You name must contain only letters")
        return last_name

    # Must be unique
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    # Must be unique
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    # Used for validation
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        # Passwords must be 16+ characters long or contain a digit
        if len(password1) < 16 and not any(char.isdigit() for char in password1):
            raise ValidationError("You password must either be 16+ letters long or contain a digit.")

        return password2

    # Save a new user and set their Group to Volunteer
    def save(self, commit=True):
        try:
            user = User.objects.create_user(
                self.cleaned_data['username'],
                self.cleaned_data['email'],
                self.cleaned_data['password1'],
            )
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            volunteer = Group.objects.get(name='Volunteer')
            volunteer.user_set.add(user)
            return user
        except Exception as e:
            raise
